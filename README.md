# 🎤 standup-transcribe

脱口秀视频转录 + 喜剧技巧标注工具。

从视频/音频文件自动生成**带时间戳的字幕 Word** + **喜剧技巧标注版 Word**。

## 功能

- 🎬 **Whisper 转录**：支持 mp4/ts/mkv/avi/mov/m4a/mp3/wav 等所有 ffmpeg 支持的格式
- ✏️ **自动校对**：内置 150+ 脱口秀人名 + 20+ 关键词自动纠错（names.json 可扩展）
- 📝 **字幕生成**：带时间戳逐段文本 + 纯文本版 Word
- 🎭 **喜剧技巧标注**：基于《人人都能学会单口喜剧》五维度体系，支持 18+ 种技巧类型
- 📊 **批量处理**：一次处理多个视频文件

## 五维度标注体系

融入教主《人人都能学会单口喜剧》核心方法论：

1. **硬核四要素**：好笑 / 真实 / 原创 / 对话感
2. **素材五特征**：真实性 / 个人化 / 宜人度 / 熟悉度 / 普适性 / 荒谬点
3. **结构逻辑**：观点先行（议论文式结构）
4. **观点提炼**：观点 = 事实 + 负面情绪
5. **加梗技术**：Act-out / 比喻 / 类比 / 夸张 / 假设 / 混合 / Call-back

## 快速开始

### 安装依赖

```bash
brew install ffmpeg
pip install openai-whisper python-docx
```

### 使用

```bash
# 单个视频
python3 scripts/transcribe.py video.mp4

# 批量处理
python3 scripts/transcribe.py ~/Downloads/*.mp4

# 指定输出目录
python3 scripts/transcribe.py --output ~/Documents video.mp4
```

### 只做喜剧标注（已有文本）

```bash
python3 scripts/annotate.py text.txt "标题" "表演者"
```

## 人名校对

`scripts/names.json` 包含 150+ 脱口秀演员/辩手/嘉宾的名字和易混淆别名，转录时自动加载校对。

新增人名只需编辑 `names.json` 的对应分类即可。

## 喜剧技巧标注类型

| 维度 | 技巧标签 |
|------|---------|
| 结构 | 铺垫、笑点、递进、极简收束 |
| 变奏 | 反转、二次反转、解构、回旋镖 |
| 技法 | Act-out、比喻、类比、夸张、假设、混合、Call-back |
| 深度 | 观察、社会观察、自嘲 |
| 表现 | 金句、Meta笑点、钩子 |

## 依赖

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/)
- [openai-whisper](https://github.com/openai/whisper)
- [python-docx](https://github.com/python-openxml/python-docx)

## License

MIT
