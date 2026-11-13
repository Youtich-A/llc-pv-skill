# 组件、调用与搬迁

## 包内可执行组件

- `components/video-watch/vw.py`：通用量测、采样、图版、连续序列、原图面板、按需OCR/ASR。
- `components/video-watch/vwtools.py`：逐帧解码、连通域和差分等辅助管道。
- [video-watch操作说明](../components/video-watch/OPERATIONS.md)：按需查看子命令，参数以当前脚本`--help`为准。
- `components/video-watch/LICENSE`：MIT，上游作者CFITSec，保留版权与许可。
- `scripts/audit_rgba_sequence.py`：从本地复刻工作流迁入的只读PNG序列诊断。
- [AE MCP操作组件](../components/aftereffects-mcp/OPERATIONS.md)：便携连接、操作、工具参数及ES3参考；不捆绑服务端运行时。

先定位当前技能根目录，再运行`python <skill-root>/components/video-watch/vw.py doctor`；Windows可用实际Python解释器或`py -3`。外部依赖需要Python、完整FFmpeg/ffprobe、ImageMagick及字体；numpy/Pillow用于额外量测，OCR/ASR及模型按需。包不携带大型二进制或模型，迁移后必须重新doctor。不要复制旧机器配置路径。本包建议Python 3.10+；实际测试版本见发布报告，未完成跨版本/跨平台兼容矩阵。

AE、Blender、图像工具与控制服务依目标环境确认。没有模型或软件访问能力就说明缺项；用户指定模型是否可用须实际查证，不能把某次任务的选择变成所有接收者的默认前提。

## 调用

使用`$llc-pv-skill`或“使用llc-pv-skill”调用。安装方法见[INSTALL.md](../INSTALL.md)。

## 方法来源与运行边界

分段、逐镜、母音轨、五层动画、空间/光学、三轮与反馈方法由多个复刻案例归纳，已写入本包。案例只保留可迁移方法，不含个人对话、署名、工程位置或素材。运行无需取得开发工作区。

video-watch和AE参考组件的许可、快照来源状态与哈希见[第三方声明](../THIRD_PARTY_NOTICES.md)和[来源清单](../provenance.json)。原始媒体、AEP、角色资产、机器日志不发布。

## 能力边界

流程门禁由指令和文件状态约束，并未安装宿主级拦截器。技能不能自动清空上下文，不能替用户宣布审美通过。三轮检查、机器解码、用户评价分别记录。可编辑性要说明分工：AE图层、外部模型源文件、透明序列分别是什么，不能把有AEP说成所有内容都AE原生。

## 可选 PSD2Live

[接入参考](../components/psd2live/OPERATIONS.md)与[L2D制作流程](l2d_workflow.md)随包携带；应用与MCP代理不携带。用户肯定选择后按需从官方GitHub取得，已安装可用版本直接复用。独立调用L2D不要求接入AE。
