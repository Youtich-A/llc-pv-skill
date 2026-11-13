# 缺少组件时的下载渠道与手动接入

只在对应组件缺失时加载。已有可用环境直接沿用。区分“未安装”“已安装但宿主未暴露工具”“网络/权限受限”，不要全部归为缺MCP。

## AE MCP

官方渠道：

- [GitHub仓库与安装说明](https://github.com/kumoproductions/mcp-aftereffects)
- [GitHub Releases](https://github.com/kumoproductions/mcp-aftereffects/releases)
- [npm包](https://www.npmjs.com/package/@kumoproductions/mcp-aftereffects)
- [Node.js下载](https://nodejs.org/en/download)：本参考服务需要Node >=24。

本包参考固定版本为0.3.2。具体支持平台、版本和安装方法按该版官方说明核对。npm页面打不开不等于npm注册表或GitHub不可用；分别说明实际失败位置，不反复请求同一被阻止页面。

正常联网时，可以按[AE连接说明](ae_environment.md)的MCP配置运行`npx -y @kumoproductions/mcp-aftereffects@0.3.2`。这是MCP客户端启动服务的命令，不是粘贴到终端后就能让模型自动获得工具；还需宿主注册、重连和工具发现。

若希望先安装本地固定版本，可在用户选择的独立目录执行：

```text
npm install --prefix <local-install-dir> @kumoproductions/mcp-aftereffects@0.3.2
```

`<local-install-dir>`是需要用户/执行者替换的参数，不是可原样执行的路径。保留锁文件，将宿主的stdio启动命令指向Node，args指向该安装目录中包的`dist/index.js`。本地绝对路径只留本地配置，不提交仓库。

受限时：

1. 给出上面的官方链接及需要的版本，让用户通过可联网浏览器或机器下载。
2. GitHub源码ZIP和npm tarball通常不包含全部Node依赖；仅复制源码不能保证离线运行。需要在相同系统/架构、兼容Node环境完成依赖安装（源码还需按官方说明构建），再迁移完整运行目录；更稳妥的是由联网机器/管理员按包管理器流程准备离线缓存。
3. 下载或安装权限不足时，提供用户级目录接入选项；仍受组织策略限制时说明需要管理员完成的具体一步，不绕过限制。
4. 用户提供本地目录后，核对版本、入口和依赖，再补MCP配置。重连后调用真实工具确认目标AE，不能把文件存在当连接成功。

## video-watch

**优先使用本技能已经携带的组件，不要求另外安装一个同名全局skill：**

- `components/video-watch/vw.py`
- `components/video-watch/vwtools.py`
- `components/video-watch/OPERATIONS.md`
- `components/video-watch/LICENSE`

组件不完整时，从维护者提供的本技能完整发布ZIP重新取得上述目录，保留许可。当前包尚无经核实的video-watch原始仓库/commit，也未配置本项目公开下载页；不得编造GitHub地址，或把搜索到的同名仓库当成原组件。给出包内准确位置，并请用户提供维护者发布包/可信来源，或由维护者补发完整目录。

如果只有执行能力受限，用户可以在自己的机器解压本技能、按下方渠道准备依赖，再运行：

```text
python components/video-watch/vw.py doctor
python components/video-watch/vw.py probe <reference-video> --out <project-output-dir>
```

命令以技能根目录为当前目录，尖括号参数需替换；Windows可以使用实际解释器或`py -3`。需要后续图版时按包内操作说明执行，把图版和manifest一起保留。只能取得外部生成的证据时，注明来源、范围与未独立核验项，不宣称已亲自运行组件。

## 视频依赖下载

- [Python官方](https://www.python.org/downloads/)：本包建议Python 3.10+；可使用已有兼容版本。
- [FFmpeg官方下载入口](https://ffmpeg.org/download.html)：按平台选择该页列出的构建渠道，需要ffprobe和完整滤镜；装完运行doctor，不能仅凭能打印版本判定完整。
- [ImageMagick官方下载](https://imagemagick.org/script/download.php)：检查当前平台入口与字体。
- numpy、Pillow为扩展量测依赖；ASR/OCR及模型按需安装，未需要时不增加下载任务。

受限环境可由用户先下载/安装，再在本地video-watch配置中填写实际程序路径。配置含机器路径，不随开源包分发。首次ASR模型下载也可能需要网络；不能保证安装Python依赖后即完全离线可用。

## 缺项时的交付格式

每次至少说明：缺什么、影响哪个阶段、下载渠道/包内位置、安装或解压到哪里、完成后如何恢复。能独立推进的任务继续；依赖缺失的AE制作或视频观察保持待完成，禁止伪造检查通过。
