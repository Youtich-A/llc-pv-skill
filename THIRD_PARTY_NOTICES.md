# 第三方声明与权利范围

## video-watch

- 文件：`components/video-watch/vw.py`、`vwtools.py`和`OPERATIONS.md`。
- 本次来源：本地获得的video-watch快照；许可文件声明Copyright (c) 2026 CFITSec、MIT。
- 原许可：[components/video-watch/LICENSE](components/video-watch/LICENSE)。
- 说明：保留代码原貌；操作说明补充了计费估算不适用于所有模型的说明。文件SHA-256记录在[来源清单](provenance.json)。2026-11-13核对官方仓库 https://github.com/CFITCorporation/video-watch-skill ：LICENSE和vwtools.py与当时main一致；包内vw.py与当时main有差异，历史快照commit仍未确认，不宣称本包等同最新版上游。

## After Effects MCP

- 上游：https://github.com/kumoproductions/mcp-aftereffects 。
- 包：`@kumoproductions/mcp-aftereffects`；参考接口0.3.1，新接入示例固定0.3.2。
- 许可：MIT，Copyright (c) 2026 kumo.productions, Inc.；原文见[组件许可](components/aftereffects-mcp/LICENSE)。
- 包内内容：根据上游接口及已有操作笔记整理的便携说明、工具/操作/helper快照；删除了个人机器状态并加入版本与schema边界。
- 不包含服务端运行时、MCP SDK、Node依赖或Adobe安装文件。使用者单独取得这些依赖；它们不因项目MIT许可而变更许可。

## 外部工具与内容

Python、Node.js、FFmpeg、ImageMagick、OCR/ASR模型、字体、AE、插件及图像生成服务均由运行环境提供，不在包内分发。FFmpeg等工具的许可可能随实际构建而变，若以后捆绑二进制需另行核对。

MOTTAI、アイス、衛星仅为方法经验案例名，包内无其视频、音乐、角色图片、工程及字体。项目MIT不授予案例内容、商标或人格权益的使用许可。Adobe与After Effects为Adobe的商标，本项目为独立非官方工作流。

## PSD2Live（可选外部组件）

官方项目：https://github.com/tsunehimatoi/psd2live ，上游当前声明 GPL-3.0。本仓库只含原创流程、模板与链接，不分发其源码、二进制、MCP代理或任何角色模型。使用者按需取得并遵循所下载版本的许可；本项目MIT不更改上游许可。
