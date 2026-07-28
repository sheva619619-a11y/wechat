# -*- coding: utf-8 -*-
"""将日更 HTML 推送到微信公众号草稿箱（不群发、不发布）。"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # 公众号/
ENV_PATH = Path(__file__).resolve().parent / ".env"


def load_env(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def http_json(url: str, payload: dict | None = None, method: str = "GET") -> dict:
    body = None
    headers = {"User-Agent": "yujia-wechat-draft/1.0"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
        method = "POST"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {err}") from e


def http_upload(url: str, field: str, file_path: Path) -> dict:
    boundary = "----YujiaBoundary7MA4YWxk"
    filename = file_path.name
    data = file_path.read_bytes()
    ctype = "image/png" if filename.lower().endswith(".png") else "image/jpeg"
    parts = [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'.encode(),
        f"Content-Type: {ctype}\r\n\r\n".encode(),
        data,
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    body = b"".join(parts)
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "yujia-wechat-draft/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_access_token(app_id: str, app_secret: str) -> str:
    q = urllib.parse.urlencode(
        {"grant_type": "client_credential", "appid": app_id, "secret": app_secret}
    )
    url = f"https://api.weixin.qq.com/cgi-bin/token?{q}"
    data = http_json(url)
    if "access_token" not in data:
        raise RuntimeError(f"获取 access_token 失败: {data}")
    return data["access_token"]


def parse_meta_from_md(md_path: Path) -> tuple[str, str]:
    """从正文.md 提取推荐标题与摘要。"""
    text = md_path.read_text(encoding="utf-8")
    title = ""
    # 推荐标题行：**xxx**（推荐）
    m = re.search(r"\d+\.\s+\*\*(.+?)\*\*（推荐）", text)
    if m:
        title = m.group(1).strip()
    if not title:
        m = re.search(r"^#\s+正文[^\n]*\n", text, re.M)
        # fallback: HTML <title>
    digest = ""
    m2 = re.search(r"##\s*摘要[^\n]*\n+(.+?)(?:\n##|\n\n##)", text, re.S)
    if m2:
        digest = re.sub(r"\s+", "", m2.group(1).strip())[:120]
    return title, digest


def parse_title_from_html(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return "未命名稿件"


def extract_body_section(html: str) -> str:
    """尽量只取正文 section，去掉 html/head/body 外壳。"""
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.I | re.S)
    content = m.group(1).strip() if m else html
    # 微信草稿对外层限制较少，保留内联样式 section 即可
    return content


def rewrite_local_images(
    content: str, day_dir: Path, token: str, dry_run: bool
) -> str:
    """把 src=\"配图/xxx.png\" 换成微信 CDN URL。"""

    def repl(match: re.Match) -> str:
        src = match.group(1)
        if src.startswith("http://") or src.startswith("https://"):
            return match.group(0)
        local = (day_dir / src).resolve()
        if not local.exists():
            # 尝试相对 day_dir
            alt = day_dir / Path(src).name
            local = alt if alt.exists() else local
        if not local.exists():
            print(f"[warn] 图片不存在，跳过: {src}", file=sys.stderr)
            return match.group(0)
        if dry_run:
            print(f"[dry-run] 将上传正文图: {local.name}")
            return f'src="https://example.invalid/{local.name}"'
        url = (
            "https://api.weixin.qq.com/cgi-bin/media/uploadimg"
            f"?access_token={urllib.parse.quote(token)}"
        )
        resp = http_upload(url, "media", local)
        if "url" not in resp:
            raise RuntimeError(f"上传正文图失败 {local.name}: {resp}")
        print(f"[ok] 正文图 → {local.name}")
        return f'src="{resp["url"]}"'

    return re.sub(r'src=["\']([^"\']+)["\']', repl, content, flags=re.I)


def upload_thumb(token: str, cover: Path, dry_run: bool) -> str:
    if dry_run:
        print(f"[dry-run] 将上传封面: {cover}")
        return "THUMB_MEDIA_ID_DRY_RUN"
    url = (
        "https://api.weixin.qq.com/cgi-bin/material/add_material"
        f"?access_token={urllib.parse.quote(token)}&type=image"
    )
    resp = http_upload(url, "media", cover)
    mid = resp.get("media_id")
    if not mid:
        raise RuntimeError(f"上传封面失败: {resp}")
    print(f"[ok] 封面 media_id={mid}")
    return mid


def draft_add(
    token: str,
    *,
    title: str,
    author: str,
    digest: str,
    content: str,
    thumb_media_id: str,
    dry_run: bool,
) -> str:
    if len(title) > 32:
        print(f"[warn] 标题超过 32 字，将截断: {title}", file=sys.stderr)
        title = title[:32]
    if len(digest) > 120:
        digest = digest[:120]
    payload = {
        "articles": [
            {
                "article_type": "news",
                "title": title,
                "author": author[:16],
                "digest": digest,
                "content": content,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }
    if dry_run:
        print("[dry-run] draft/add payload keys ok")
        print(json.dumps({"title": title, "digest": digest, "author": author}, ensure_ascii=False))
        return "DRY_RUN_MEDIA_ID"
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={urllib.parse.quote(token)}"
    resp = http_json(url, payload)
    mid = resp.get("media_id")
    if not mid:
        raise RuntimeError(f"draft/add 失败: {resp}")
    return mid


def main() -> int:
    ap = argparse.ArgumentParser(description="推送日更到微信草稿箱")
    ap.add_argument("--date", required=True, help="日期目录 YYYY-MM-DD")
    ap.add_argument("--dry-run", action="store_true", help="只校验不写入")
    ap.add_argument("--html", default="", help="自定义 html 路径")
    args = ap.parse_args()

    env = {**load_env(ENV_PATH), **os.environ}
    app_id = env.get("WECHAT_APP_ID", "").strip()
    app_secret = env.get("WECHAT_APP_SECRET", "").strip()
    author = env.get("WECHAT_AUTHOR", "羽嘉低空科技").strip() or "羽嘉低空科技"

    day_dir = ROOT / "published" / args.date
    html_path = Path(args.html) if args.html else day_dir / "公众号.html"
    md_path = day_dir / "正文.md"
    cover = day_dir / "配图" / "00-封面.png"

    if not html_path.exists():
        print(f"缺少 HTML: {html_path}", file=sys.stderr)
        return 1
    if not cover.exists():
        print(f"缺少封面: {cover}", file=sys.stderr)
        return 1
    if not args.dry_run and (not app_id or not app_secret):
        print(
            f"请先配置 {ENV_PATH}（参考 .env.example）中的 WECHAT_APP_ID / WECHAT_APP_SECRET",
            file=sys.stderr,
        )
        return 1
    if args.dry_run and (not app_id or not app_secret):
        print("[dry-run] 未配置 AppID/Secret，仅校验本地文件与标题解析")

    html = html_path.read_text(encoding="utf-8")
    title, digest = ("", "")
    if md_path.exists():
        title, digest = parse_meta_from_md(md_path)
    if not title:
        title = parse_title_from_html(html)
    if not digest:
        digest = title[:54]

    print(f"目录: {day_dir}")
    print(f"标题: {title}")
    print(f"摘要: {digest}")

    token = "DRY" if args.dry_run else get_access_token(app_id, app_secret)
    if not args.dry_run:
        print("[ok] access_token 已获取")

    content = extract_body_section(html)
    content = rewrite_local_images(content, day_dir, token, args.dry_run)
    thumb = upload_thumb(token, cover, args.dry_run)
    media_id = draft_add(
        token,
        title=title,
        author=author,
        digest=digest,
        content=content,
        thumb_media_id=thumb,
        dry_run=args.dry_run,
    )
    print(f"\n完成。草稿 media_id = {media_id}")
    print("请到微信公众平台 → 草稿箱 人工复核后发布（脚本不会自动群发）。")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        raise SystemExit(2)
