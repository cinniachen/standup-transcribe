# 发布到在线文档

发布是最后一步，不是核心步骤。无论上传是否成功，都要先保留本地文件。

## 上传前提醒

上传前必须提醒用户：

```text
这个文档会包含视频转录和学习分析，可能涉及私人素材或版权内容。确认要上传到云文档吗？
```

用户确认后再上传。

## 推荐发布流程

1. 生成本地Word。
2. 生成本地Markdown备份。
3. 用户确认上传平台。
4. 上传到对应平台。
5. 返回在线链接和本地备份路径。

## 平台优先级

如果用户没有指定平台，不要默认上传。

如果用户说"金山文档"：

- 优先尝试封装好的 `scripts/publish_kdocs.py`。
- 如果缺少凭证，提醒设置环境变量 `KDOCS_UPLOAD_URL` 和 `KDOCS_ACCESS_TOKEN`。
- 上传失败时，不要重做转录；保留本地Word，提示用户稍后只重试上传。

如果用户说"飞书文档"：

- 使用可用的飞书文档工具或CLI。
- 仍然先保留本地备份。

如果用户说"Markdown"：

- 直接生成 `.md` 文件，适合导入Notion、Obsidian、语雀等工具。

## 金山文档脚本

```bash
python3 scripts/publish_kdocs.py 本地文档.docx --title "文档标题"
```

返回：

```json
{
  "status": "ok",
  "url": "https://...",
  "local_file": "/path/to/file.docx"
}
```

配置项必须放环境变量：

- `KDOCS_UPLOAD_URL`
- `KDOCS_ACCESS_TOKEN`

不要把密钥写进仓库。

## 成功标志

- 用户拿到在线文档链接。
- 本地仍有Word或Markdown备份。
- 失败时能只重试上传，不需要重新转录。
