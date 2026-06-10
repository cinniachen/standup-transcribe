#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金山文档发布脚本。

安全约定：
- 不把密钥写入仓库。
- 只从环境变量读取配置。
- 上传前请先取得用户确认。

需要的环境变量：
- KDOCS_UPLOAD_URL: 你的金山文档上传接口地址
- KDOCS_ACCESS_TOKEN: 访问令牌
"""

import argparse
import json
import os
import sys


def publish(file_path, title=None):
    file_path = os.path.expanduser(file_path)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    upload_url = os.environ.get("KDOCS_UPLOAD_URL")
    token = os.environ.get("KDOCS_ACCESS_TOKEN")
    if not upload_url or not token:
        raise RuntimeError(
            "还没有配置金山文档上传环境变量。请先设置 KDOCS_UPLOAD_URL 和 KDOCS_ACCESS_TOKEN。"
        )

    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("缺少 requests，请先安装：pip install requests") from exc

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        data = {"title": title or os.path.splitext(os.path.basename(file_path))[0]}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(upload_url, headers=headers, data=data, files=files, timeout=120)

    if response.status_code >= 400:
        raise RuntimeError(f"金山文档上传失败: {response.status_code} {response.text[:500]}")

    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text}

    url = payload.get("url") or payload.get("link") or payload.get("web_url")
    return {
        "status": "ok",
        "url": url,
        "local_file": file_path,
        "response": payload,
    }


def main():
    parser = argparse.ArgumentParser(description="上传学习笔记到金山文档")
    parser.add_argument("file", help="本地Word/Markdown文件")
    parser.add_argument("--title", default=None, help="在线文档标题")
    args = parser.parse_args()

    try:
        result = publish(args.file, args.title)
    except Exception as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
