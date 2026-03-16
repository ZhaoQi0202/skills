#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import requests
from PIL import Image


def load_config(path: str | None) -> dict:
    if not path:
        return {}
    cfg_path = Path(path).expanduser().resolve()
    return json.loads(cfg_path.read_text(encoding='utf-8'))


def resolve_value(cli_value, cfg: dict, *keys, default=None):
    if cli_value not in (None, ''):
        return cli_value
    current = cfg
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current if current not in (None, '') else default


def get_token(app_id: str, app_secret: str) -> str:
    r = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token',
        params={
            'grant_type': 'client_credential',
            'appid': app_id,
            'secret': app_secret,
        },
        timeout=60,
    )
    r.raise_for_status()
    body = r.json()
    token = body.get('access_token')
    if not token:
        raise RuntimeError(f'Failed to get access_token: {body}')
    return token


def compress_cover(src: Path, dest: Path) -> Path:
    img = Image.open(src).convert('RGB')
    img.thumbnail((900, 383))
    quality = 85
    while True:
        img.save(dest, format='JPEG', quality=quality, optimize=True)
        if dest.stat().st_size <= 60000 or quality <= 25:
            return dest
        quality -= 10


def upload_thumb(access_token: str, cover_path: Path) -> dict:
    with open(cover_path, 'rb') as f:
        r = requests.post(
            'https://api.weixin.qq.com/cgi-bin/material/add_material',
            params={'access_token': access_token, 'type': 'thumb'},
            files={'media': (cover_path.name, f, 'image/jpeg')},
            timeout=120,
        )
    r.raise_for_status()
    body = r.json()
    if 'media_id' not in body:
        raise RuntimeError(f'Failed to upload thumb: {body}')
    return body


def add_draft(access_token: str, article: dict) -> dict:
    payload = json.dumps({'articles': [article]}, ensure_ascii=False).encode('utf-8')
    r = requests.post(
        'https://api.weixin.qq.com/cgi-bin/draft/add',
        params={'access_token': access_token},
        data=payload,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        timeout=120,
    )
    r.raise_for_status()
    body = r.json()
    if 'media_id' not in body:
        raise RuntimeError(f'Failed to add draft: {body}')
    return body


def submit_publish(access_token: str, draft_media_id: str) -> dict:
    payload = json.dumps({'media_id': draft_media_id}, ensure_ascii=False).encode('utf-8')
    r = requests.post(
        'https://api.weixin.qq.com/cgi-bin/freepublish/submit',
        params={'access_token': access_token},
        data=payload,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def get_publish_status(access_token: str, publish_id: str) -> dict:
    payload = json.dumps({'publish_id': publish_id}, ensure_ascii=False).encode('utf-8')
    r = requests.post(
        'https://api.weixin.qq.com/cgi-bin/freepublish/get',
        params={'access_token': access_token},
        data=payload,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()




def validate_rendered_html(content: str) -> None:
    bad_patterns = [
        r'>\s*#\s+',
        r'>\s*##\s+',
        r'>\s*###\s+',
    ]
    for pattern in bad_patterns:
        if re.search(pattern, content):
            raise RuntimeError('Rendered HTML still contains Markdown heading markers. Fix article rendering before creating draft.')

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--config', help='Path to config.local.json or config.template-based local config')
    p.add_argument('--app-id')
    p.add_argument('--app-secret')
    p.add_argument('--cover')
    p.add_argument('--title')
    p.add_argument('--author', default='小五')
    p.add_argument('--digest')
    p.add_argument('--content-file')
    p.add_argument('--source-url', default='')
    p.add_argument('--draft-media-id')
    p.add_argument('--publish', action='store_true')
    p.add_argument('--publish-id')
    p.add_argument('--status', action='store_true')
    args = p.parse_args()

    cfg = load_config(args.config)
    app_id = resolve_value(args.app_id, cfg, 'wechat', 'app_id')
    app_secret = resolve_value(args.app_secret, cfg, 'wechat', 'app_secret')
    author = resolve_value(args.author, cfg, 'wechat', 'author', default='小五')
    source_url = resolve_value(args.source_url, cfg, 'wechat', 'source_url', default='')

    if not app_id or not app_secret:
        raise SystemExit('Missing app credentials. Pass --app-id/--app-secret or provide them in --config.')

    access_token = get_token(app_id, app_secret)

    if args.status:
        if not args.publish_id:
            raise SystemExit('--publish-id is required with --status')
        print(json.dumps(get_publish_status(access_token, args.publish_id), ensure_ascii=False, indent=2))
        return 0

    if args.publish:
        if not args.draft_media_id:
            raise SystemExit('--draft-media-id is required with --publish')
        print(json.dumps(submit_publish(access_token, args.draft_media_id), ensure_ascii=False, indent=2))
        return 0

    if not all([args.cover, args.title, args.digest, args.content_file]):
        raise SystemExit('Draft creation requires --cover --title --digest --content-file')

    cover_src = Path(args.cover)
    cover_tmp = Path('/tmp/wechat_mp_thumb.jpg')
    compress_cover(cover_src, cover_tmp)
    thumb = upload_thumb(access_token, cover_tmp)
    content = Path(args.content_file).read_text(encoding='utf-8')
    validate_rendered_html(content)
    forbidden_markdown = ['<p style="margin:32px 0 14px 0;font-size:20px;line-height:1.5;font-weight:700;color:#111;"># ', '>## ', '>### ', '\n# ', '\n## ', '\n### ']
    if any(marker in content for marker in forbidden_markdown):
        raise SystemExit('Rendered HTML still appears to contain Markdown heading remnants. Fix rendering before creating draft.')
    article = {
        'title': args.title,
        'author': author,
        'digest': args.digest,
        'content': content,
        'content_source_url': source_url,
        'thumb_media_id': thumb['media_id'],
        'need_open_comment': 0,
        'only_fans_can_comment': 0,
    }
    draft = add_draft(access_token, article)
    print(json.dumps({'thumb': thumb, 'draft': draft}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
