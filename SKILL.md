---
name: standup-transcribe
description: 脱口秀视频转录+喜剧技巧标注工具。支持单个或批量视频文件处理：Whisper 转录 → 自动校对人名/关键词 → 生成字幕 Word → 喜剧技巧标注版 Word。触发词：转录、转录视频、视频转字幕、脱口秀转录、喜剧标注、视频转录、音频转文字、standup transcript、comedy annotation、批量转录
metadata: {"emoji":"🎤","requires":{"bins":["ffmpeg"]}}
---

# 脱口秀转录 + 喜剧技巧标注

从视频/音频文件自动生成**带时间戳的字幕 Word** + **喜剧技巧标注版 Word**。

## 支持格式

mp4, ts, mkv, avi, mov, m4a, mp3, wav 等所有 ffmpeg 支持的音视频格式。

## 使用方式

### 方式 1：直接给我视频文件路径（推荐）

用户只需要提供视频文件路径（单个或多个），我会自动完成：

1. **提取音频** → ffmpeg 提取 16kHz wav
2. **Whisper 转录** → 生成带时间戳的逐段文本
3. **自动校对** → 修正常见人名/关键词错误（如 妙妙→鸟鸟, 张受刚→张绍刚）
4. **生成字幕 Word** → 带时间戳版本 + 纯文本版本
5. **AI 喜剧技巧标注** → 我逐段分析标注铺垫/笑点/反转/call-back/自嘲等技巧，手写高质量注释
6. **输出标注版 Word** → 精选重点段落 + 技巧类型标签 + 💡详细注释 + 技巧统计 + 风格总结

### 方式 2：命令行快速转录（不含标注）

```bash
# 单个文件
python3 ~/.workbuddy/skills/standup-transcribe/scripts/transcribe.py 视频文件.mp4

# 批量处理
python3 ~/.workbuddy/skills/standup-transcribe/scripts/transcribe.py ~/Downloads/*.mp4

# 指定输出目录
python3 ~/.workbuddy/skills/standup-transcribe/scripts/transcribe.py --output ~/Documents 视频文件.mp4
```

### 方式 3：只做喜剧标注（已有文本）

用户已有文本时，我可以直接做标注。只需提供文本内容，我会生成标注版 Word。

## AI Agent 调用指南

当用户说「帮我转录视频」「给这个视频做喜剧标注」「批量处理这几个视频」时：

### 步骤 1：转录（使用 transcribe.py）

```python
import sys
sys.path.insert(0, os.path.expanduser('~/.workbuddy/skills/standup-transcribe/scripts'))
from transcribe import process_single, process_batch

# 单个文件
output = process_single(
    video_path="/path/to/video.mp4",
    output_dir="~/Downloads",
    title="鸟鸟 - 主咖和TA的朋友们",
    corrections={"妙妙": "鸟鸟", "张受刚": "张绍刚"},  # 可选：自定义校对
    model="base"  # 可选：tiny/base/small/turbo/large-v3
)

# 批量处理
results = process_batch(
    video_paths=["/path/to/1.mp4", "/path/to/2.mp4"],
    output_dir="~/Downloads",
    corrections={"妙妙": "鸟鸟"}  # 可选
)
```

### 步骤 2：AI 喜剧标注（核心步骤 ⭐）

**重要：标注不是自动脚本完成的，而是由 AI 逐段分析手写注释。**

转录完成后，提取纯文本，然后由 AI（我自己）逐段分析：
- 精选重点段落（不需要逐行标注，只标有技巧价值的段落）
- 识别技巧类型（铺垫/笑点/反转/call-back/自嘲/递进/金句/观察/暗喻/meta笑点/社会观察 等）
- 手写高质量注释，解释每个技巧为什么好笑、怎么运作
- 生成标注版 Word 文档

生成标注版的参考格式（comedy_analysis.py 风格）：
```python
# 标注数据格式：(文本, 技巧标签, 注释说明)
segments = [
    ("大家好 我是鸟鸟", "钩子", "简洁开场，建立身份"),
    ("张伟丽觉得自己像仙人掌", "铺垫 + 暗喻", "仙人掌=外表带刺、内心柔软，与张伟丽UFC冠军形象呼应"),
    # ... 精选所有重点段落
]
```

然后调用 `generate_annotated_word` 生成 Word：
```python
sys.path.insert(0, os.path.expanduser('~/.workbuddy/skills/standup-transcribe/scripts'))
from annotate import generate_annotated_word

generate_annotated_word(
    text_lines=lines,
    title="鸟鸟《主咖和TA的朋友们》喜剧技巧标注版",
    output_path="~/Downloads/标注版.docx",
    performer="鸟鸟",
    custom_annotations=segments  # 传入 AI 精选的标注数据
)
```

**标注要点：**
- 精选比例：约 50-70% 的段落值得标注（过渡句不标）
- 注释质量：每个注释要解释"为什么好笑"和"技巧原理"，不是简单贴标签
- 分段标题：按嘉宾/话题分段，如【张绍刚】【黄圣依·CEO】【张伟丽·暴力美学】
- 风格总结：根据标注数据统计技巧分布，总结表演者个人风格（5-8条）
- 参考标杆：comedy_analysis.py 中的标注深度和注释质量

### 步骤 3：生成 segments JSON（中间文件，供标注用）

转录后如果需要中间 JSON，可以在 process_single 后加：

```python
import json
json.dump(result["segments"], open("segments.json", "w"), ensure_ascii=False, indent=2)
```

## 校对字典

内置常见脱口秀人名/关键词校对：
- 演员：鸟鸟/妙妙/牛牛/呼兰/杨笠/庞博/王建国/徐志胜/何广智/赵晓卉/李雪琴/小齐 等
- 主持人：张绍刚/李诞/大张伟
- 关键词：脱口修→脱口秀、仙人长→仙人掌、囚徒困境 等

用户可传入自定义 `corrections` 字典扩展。

## 喜剧技巧标注体系（五维度分析框架）

基于单立人喜剧教主《人人都能学会单口喜剧》核心方法论，标注体系分为五个维度：

### 维度一：核心四要素（评估基准，不作为标签）
好笑 · 真实 · 原创 · 对话——AI 在注释中逐段评估稿件是否满足这四个基石。

### 维度二：素材选择（评估维度，嵌入注释）
真实性 · 个人化 · 宜人度 · 熟悉度 · 普适性 · 荒谬点——AI 在注释中评估素材质量。

### 维度三：结构逻辑标签

| 标签 | 颜色 | 说明 |
|------|------|------|
| [引子] | 青绿 | 开场钩子，引入话题 |
| [论点] | 蓝 | 核心观点陈述（观点先行，非流水账） |
| [分论点] | 蓝 | 子论点，支持主论点 |
| [荒诞点] | 粉红 | 点出素材中的冲突/变化/不合理之处 |
| [例证] | 棕 | 用具体例子论证论点 |
| [铺垫] | 蓝 | 建立前提/背景，为笑点蓄力 |
| [收尾] | 青绿 | 收束/结束 |

### 维度四：观点标签

| 标签 | 颜色 | 说明 |
|------|------|------|
| [观点] | 金 | 观点=事实+负面情绪（困难/奇怪/害怕/愚蠢） |
| [负面情绪] | 灰蓝 | 困难/奇怪/害怕/愚蠢——观点的情绪引擎 |
| [社会观察] | 灰蓝 | 将社会现象转化为喜剧素材 |

### 维度五：加梗技术标签

| 标签 | 颜色 | 说明 |
|------|------|------|
| [笑点] | 红 | 包袱释放点 |
| [呈现] | 绿 | Act-out，直接"演出来"而非转述 |
| [比喻] | 紫 | "就像……"产生画面感 |
| [类比] | 紫 | 用另一事物解释当下的荒谬感 |
| [夸张] | 粉红 | 局部夸大事实，制造不合理 |
| [假设] | 蓝 | 动机假设/后果假设 |
| [混合] | 深紫 | 不相关甚至对立的事物联系，产生错位 |
| [call-back] | 橙 | 首尾呼应，回收前面提到的梗 |
| [反转] | 深紫 | 打破观众预期 |
| [二次反转] | 深紫 | 反转之后再反转 |
| [自嘲] | 绿 | 自我调侃，建立亲和力 |
| [金句] | 金 | 点睛之笔，简洁有力 |
| [递进] | 青 | 层层递进，逐步升级 |
| [反讽] | 深灰 | 正话反说 |
| [meta笑点] | 金 | 元喜剧：调侃表演本身 |
| [解构] | 深紫 | 解构常见概念，制造荒诞 |
| [极简收束] | 青绿 | 极短收尾，节奏反差 |
| [误导] | 蓝 | 引导到错误方向 |
| [悬念] | 蓝 | 制造期待 |
| [观察] | 棕 | 生活细节提炼 |
| [暗喻] | 紫 | 比喻的隐式用法 |
| [对比] | 灰蓝 | 对照制造落差 |
| [排比] | 青 | 节奏递进增强力度 |

### AI 标注要点

- **结构**：标注是"议论文"还是"记叙文"模式？引子→论点→荒诞点→例证是否清晰？
- **观点**：是否符合"观点=事实+负面情绪"公式？深度如何？
- **素材**：真实性/个人化/宜人度/熟悉度/普适性评估，荒谬点挖掘是否充分？
- **加梗**：用了哪些加梗技术？呈现/比喻/类比/夸张/假设/混合/call-back 的分布？
- **精简**：是否有冗余信息？是否符合"餐巾纸原则"？

## 环境要求

- Python 3.10+
- ffmpeg（`brew install ffmpeg`，或放置在 `~/FFmpeg/ffmpeg`）
- openai-whisper（`pip install openai-whisper`）
- python-docx（`pip install python-docx`）
