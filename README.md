# 🎤 standup-transcribe

把脱口秀视频/音频变成能复盘、能练习的喜剧技巧学习笔记。

## 功能

- 🎬 **Whisper转录**：支持mp4/ts/mkv/avi/mov/m4a/mp3/wav等所有ffmpeg支持的格式
- ✏️ **自动校对**：内置150+脱口秀人名+20+关键词自动纠错（names.json可扩展）
- 📝 **学习笔记生成**：bit块拆分、五维技巧标注、为什么好笑、可迁移写法、创作练习题
- 🎭 **五维标注体系**：基于《人人都能学会单口喜剧》核心方法论
- 📊 **批量处理**：每个视频单独笔记+合集学习包
- ☁️ **可选云发布**：支持金山文档、飞书、Markdown，默认只生成本地文件

## 快速开始

### 安装依赖

```bash
brew install ffmpeg
pip install openai-whisper python-docx
```

### 转录

```bash
python3 scripts/transcribe.py video.mp4
python3 scripts/transcribe.py -o ~/Documents video.mp4 --segments-json
python3 scripts/transcribe.py video1.mp4 video2.mp4
```

### 生成学习笔记

```bash
python3 scripts/annotate.py segments.json --title "表演者 - 场次" --performer "表演者" --format md
```

### 上传金山文档（可选）

```bash
# 先设置环境变量：KDOCS_UPLOAD_URL / KDOCS_ACCESS_TOKEN
python3 scripts/publish_kdocs.py 本地笔记.docx --title "标题"
```

## 人名校对

`scripts/names.json`包含150+脱口秀演员/辩手/嘉宾的名字和易混淆别名。新增人名编辑对应分类即可。

## License

MIT
