# llc-pv-skill

版本0.4.0-alpha.1。按参考复刻文字PV、角色手书和MV，支持换角色。旧称`llc_pv_skill`；标准发行目录和标识改为`llc-pv-skill`，避免严格宿主拒绝下划线名称。

## 解压与部署

解压后将[INSTALL.md](INSTALL.md)交给有本地文件/命令能力的AI，内含可直接复制的部署请求。可复制整个目录或使用默认只预览的安装器。刷新会话后调用`$llc-pv-skill`或“使用llc-pv-skill复刻这段PV”。旧称及`/llc_rb_pv`兼容为文字口令，不自动注册客户端命令。

## 工作流程

环境核查 → 全片video-watch与章节标记 → 约20秒、尽量不超过25秒自然分段 → 逐镜高密度脚本（过长拆事件，制作时分开读）→ 素材核对 → 个体/父级/空间/镜头分别制作 → 三轮逐次全片对照、完整问题集修复与回归 → 预览 → 用户明确肯定 → 下一段。

前奏、间奏、副歌精度更高，主歌仍须完整。强烈优先评估2.5D/3D、前后遮挡、背景四角与画外余量。每字检查入场、持有发展和出场，不能整句捆绑。不明风格化询问用户特效、图片或截图路线。普通零散自查低于正式三轮；“马上导出”不自动取消三轮。

## 内容与依赖

包内含主技能、按需参考、项目/章节/镜头/审查模板、video-watch脚本与说明、AE MCP便携参考、安装器、扫描器及许可。所有运行引用随包定位，不依赖开发者工程。

外部需兼容Python（建议3.10+）、完整FFmpeg/ffprobe、ImageMagick和字体。扩展量测/透明序列诊断需[NumPy与Pillow](requirements.txt)，OCR/ASR按需。AE制作需合法可用的AE、Node.js >=24及[AE MCP](https://github.com/kumoproductions/mcp-aftereffects)；新接入示例固定0.3.2，以实际schema为准。

不捆绑Adobe、MCP服务端、生图模型、密钥、字体、案例视频/音乐、截图、AEP或角色资产。安装技能不等于AE控制已部署或制作质量通过。

## 隐私、许可和测试边界

只转发新ZIP或技能目录，不转发上级工作区、旧包和备份。[SECURITY.md](SECURITY.md)说明本地/模型服务数据边界；[RELEASE_REVIEW.md](RELEASE_REVIEW.md)记录检查范围。

工作流与脚本采用[MIT](LICENSE)，第三方保留[原许可](THIRD_PARTY_NOTICES.md)，[来源](provenance.json)可核查。许可不授予歌曲、角色、字体或其他输入素材权利。本版是alpha；结构、隐私、解压/安装和工具冒烟不等于跨平台AE端到端验收或逐像素保证。

## L2D 子功能

可单独说“使用 llc-pv-skill 的 L2D 功能”，或在复杂角色动画制作中进入。先确认是否采用 [PSD2Live](https://github.com/tsunehimatoi/psd2live)，再明确拆分工具、拆法和 PSD 准备方。产物包含分层源、可重开原生工程及预览；颈根约束与衣领遮挡是必查连接点。组件按需获取，未捆绑其 GPL 软件。

## 模型与自检

三轮要求相同；DeepSeek/Kimi/GLM 等默认使用加强记录约束，GPT/Gemini/Claude 等默认精简辅助，用户可覆盖。减少三轮之外的重复整体观看，不减少正式三轮。详细规则见 [执行强度](references/review_execution.md)。

## 开发与公开发布

此目录就是可上传的仓库根目录。只上传此目录，不上传上级素材工作区。GitHub 上传由使用者另行执行。

```text
python scripts/check_release.py . --git-worktree
python scripts/validate_review.py --help
python -B -m unittest discover -s tests
```

`evals/evals.json` 含不依赖私人媒体的行为评估场景。自动检查验证元数据、链接、隐私启发式、记录一致性与脚本行为，不保证模型执行质量；行为场景需由实际调用模型评估。通用宿主可读取 SKILL.md，Codex 元数据在 agents/openai.yaml。
