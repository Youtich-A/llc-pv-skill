# 解压后交给AI部署

## 可直接复制给本地AI的请求

> 请读取此解压目录中的INSTALL.md和SKILL.md，将llc-pv-skill部署到我当前AI宿主支持的本地技能目录。先识别宿主、系统、实际Python和已有依赖，不照搬另一台机器的路径。运行包内发布检查，预览安装计划，按本次部署请求安装技能并验证复制完整性。已有旧版先检查并备份，不清空其他技能或覆盖整份宿主配置。检查video-watch依赖；需要AE制作时再按包内参考接入AE MCP，先只读确认正确实例。说明完成项、缺项和需要我操作的一步。当前只部署，不开始制作，不上传本地项目。

宿主具体技能目录、MCP配置格式和刷新方式按其实际界面/文档核实。`agents/openai.yaml`为可选宿主元数据，其他宿主可忽略。未支持技能机制的客户端可让模型按文件读取工作流，但不能声称自动发现已成功。

## 1. 安装技能

当前目录为解压后的`llc-pv-skill`。尖括号参数须替换；`python`可换本机解释器，Windows可用已安装的`py -3`。

```text
python scripts/check_release.py . --git-worktree
python scripts/install_skill.py --skills-dir <宿主实际技能目录>
```

安装命令默认只预览。核对路径后执行：

```text
python scripts/install_skill.py --skills-dir <宿主实际技能目录> --apply
```

目标为该目录下的`llc-pv-skill/`。已存在时默认拒绝覆盖；明确更新用`--replace --apply`，旧版备份到技能目录外的`skill-install-backups/`。安装器不下载依赖、不改宿主/MCP配置、不删除其他技能。Git克隆目录的`.git`元数据不会复制进安装目录；`--git-worktree`仅跳过元数据扫描，不代表审计过Git历史。也可手动复制整个标准目录；不要只复制SKILL.md，或重复套两层同名目录。

旧的`llc_pv_skill`目录不会自动移走；若新旧同时被宿主识别，先查看版本，备份到技能目录之外，再由本次部署执行者停用旧副本，避免双份触发。不要直接删除旧版。

安装后刷新技能列表或开启新会话，检查标准名是否可见。无法验证宿主发现时如实标记“文件已安装，宿主发现待验证”。

## 2. 视频观察依赖

```text
python components/video-watch/vw.py doctor
```

需要兼容Python（建议3.10+）、完整FFmpeg/ffprobe、ImageMagick和字体。缺项按[下载说明](references/downloads.md)提供官方渠道。扩展量测/序列诊断需NumPy与Pillow；优先沿用已兼容环境，缺少时在独立虚拟环境安装[requirements.txt](requirements.txt)：

```text
python -m venv <用户选择的环境目录>
<该环境的python> -m pip install -r requirements.txt
```

doctor后还需用获授权短片完成probe/grid并实际查看。运行结果和`vw.config.json`留在用户项目或本地配置目录，不能回写发行包。基础链可离线运行；ASR/OCR按需安装，首次取得模型可能联网。

## 3. 按需接入AE

先读[AE环境与连接](references/ae_environment.md)、[操作组件](components/aftereffects-mcp/OPERATIONS.md)。已有可用服务直接沿用。缺失时按[上游说明](https://github.com/kumoproductions/mcp-aftereffects)与[下载参考](references/downloads.md)安装固定版本和当前客户端stdio配置。

新接入示例为`@kumoproductions/mcp-aftereffects@0.3.2`，需要Node.js >=24；不自动升级已有环境。实际工具名可能带宿主前缀，操作以`ae_catalog`为准。先只读`ae_context`/`ae_version_info`确认目标；制作授权范围内再用工作副本验证写入和多帧渲染。使用者准备AE及脚本权限，不替用户接受许可或放开无关权限。

下载成功、服务端已安装、宿主已注册MCP、模型看到工具、AE读取成功、写入与渲染成功分别记录。需要宿主重启或用户操作时明确指出，不能假报可用。

## 4. alpha首测

用获授权的约10–20秒短片（单工作段尽量不超过25秒）测试首段，提供参考路径、范围和目标。先读全片、写逐镜脚本，不确定效果向用户询问；完成三轮实际观看和问题闭环再评估画面。ZIP/安装成功不等于制作通过。

反馈用镜头/时间、问题描述和允许公开的裁切；不要公开凭据、真实配置、完整日志和未公开素材。

## 5. 可选 L2D 功能

调用“使用 llc-pv-skill 的 L2D 功能”，按[L2D流程](references/l2d_workflow.md)确认需要后，才从官方来源按需取得 PSD2Live。现有可用安装可复用。只安装本技能不自动安装 PSD2Live，不修改任何账号或客户端全局设置。
