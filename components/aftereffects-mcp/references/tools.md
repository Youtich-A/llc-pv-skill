
# MCP 工具参数（11 个）

来源：0.3.1版本`tools/list`参考快照（protocolVersion `2024-11-05`）。工具前缀依MCP宿主而定；一种常见形态为：
`mcp__aftereffects__<name>`。所有工具都有一个可选的 `instance` 参数（多实例寻址），下表省略不重复。

`instance` 语义（原文）：

> After Effects instance to address for this call, when several are running (AfterFX.exe -m):
> an instance id (its AE_MCP_INSTANCE at launch, or the `name` given to instance.start) or the name
> of the project file it has open. Omit to use this server's default (AE_MCP_INSTANCE, else the single
> live instance). ae_context and ae_do instance.list show what is live.

---

## ae_context

- 注解：`readOnlyHint: true`
- 参数：无（仅 `instance`）
- 用途：会话开始摸底。返回 `project`（file/dirty/numItems/bitsPerChannel）、`instance`、`activeComp`、
  `selectedLayers`、`helpers[]`（`AE.*` 清单）、`es3Rules[]`、`tips[]`、`undoContract[]`、`items[]`、
  `transport`、`instances[]`。

## ae_version_info

- 注解：`readOnlyHint: true`
- 参数：无（仅 `instance`）
- 返回：`app`（version/buildName/buildNumber/language/memoryInUse/availableGPUs）、
  `capabilities`（saveFrameToPng/appEffects/bridgeTalk/socket）、`project`（numItems/file/dirty）、
  `agent`、`server.exportSchemaVersion`。

版本与能力由当前ae_version_info返回，不能从本参考推定。

## ae_catalog

- 注解：`readOnlyHint: true`
- 参数：`category?: string`
- 行为：不带 `category` → 列出全部类别 + 操作数 + 操作名 + `totalOperations` + `policy` + `undo` 说明；
  带 `category` → 列出该类别每个操作的详细参数。
- 返回示例：`{ ok, categories: [{category, operationCount, operations[]}], totalOperations, policy, undo }`

## ae_project_info

- 注解：`readOnlyHint: true`
- 参数：无（仅 `instance`）
- 用途：工程级信息（文件路径、dirty、全部条目及类型/摘要、活动条目）。**从这里开始。**

## ae_comp_info

- 注解：`readOnlyHint: true`
- 参数：
  - `nameOrId` **必填** — 合成名（精确匹配）或数字 item id，**或由它们组成的数组**（一次取多个合成）
- 返回：尺寸、fps、时长、工作区、运动模糊、图层摘要。

## ae_layer_info

- 注解：`readOnlyHint: true`
- 参数：
  - `compNameOrId` **必填** — 合成名（精确匹配）或数字 item id
  - `layerIndex` **必填** — 1-based 图层序号，**或序号数组**，**或字符串 `'all'`**
  - `includeProperties?: boolean` — 默认 `true`；设 `false` 直接跳过属性树遍历
  - `detail?: 'full' | 'summary'` — 默认 `full`。`summary` 丢掉仍是默认值（无关键帧、无表达式、从未改过）
    的属性，通常小 5–10 倍；组骨架保留，所以效果/蒙版仍可见。**审计先从 `summary` 开始**，
    完整属性树单层常 >100KB。
- 返回：变换、效果、蒙版、文本、形状内容、关键帧（含插值名与贝塞尔 ease 的 speed/influence）。

## ae_do

- 注解：`destructiveHint: true`
- 参数：
  - `operation` **必填** — `ae_catalog` 里的操作名，如 `layer.create_solid`、`keyframe.add`
  - `args?: object` — 操作参数；按 `ae_catalog` 声明的参数校验，缺必填/类型错/未知键在联系 AE 前就拒绝。
    零参操作可省略。
  - `timeoutMs?: integer` — 单次调用超时，默认 `60000`。`render.start`、大型 `batch.run` 需要调高。
- 关键行为（原文摘要）：
  - 多个操作**包进一个 `batch.run`**，不要连发多次 `ae_do`；读取/校验步骤（`comp.info`、`layer.info`、
    `render.frame`）可以搭同一个 batch。
  - 每次调用自动包成**一个** undo 组；`batch.run` 算一次调用 = 一个撤销步。
    **绝不要**在代码里 `app.beginUndoGroup`/`endUndoGroup`。
  - 例外：undo/redo 自身（`project.undo`、`command.execute` 16/2035）跑在组外，必须单独调用，
    不能进 `batch.run`。
  - 响应附带环境上下文（活动合成、选中图层、工程状态），零额外往返。
- 示例（原文）：
  ```json
  { "operation": "keyframe.add",
    "args": { "comp": "Main", "layer": 1, "property": ["Transform","Position"], "time": 2, "value": [960,540] } }
  ```

## ae_render_frame

- 注解：`destructiveHint: false`
- 参数：
  - `compNameOrId` **必填** — 合成名或数字 item id
  - `time?: number` — 渲染的秒数；与 `times` 二选一
  - `times?: number[]` — 多个时间点，**一次调用**渲染；文件写成 `<outPath stem>_<index><ext>`，
    在 `frames` 里按索引对齐返回。1–32 项。
  - `outPath` **必填** — PNG 绝对路径；父目录不存在会自动创建。配 `times` 时作为命名主干。
  - `useDisplayStartTime?: boolean` — `true` 时时间相对 `comp.displayStartTime`，默认 `false`
  - `colorManaged?: 'auto' | 'off'` — `auto`（默认）检测工作空间，返回 viewer 准确、带 sRGB 标记的
    8-bit PNG；`off` 是旧的 16-bit 未标记、工作空间数值输出（在色彩管理工程里看起来偏暗/偏色）
  - `analyze?: boolean` — 对每个捕获做测量：四边均匀色带（宽度 + 透明/颜色 —— 黑边、信箱、空边距）、
    非背景像素包围盒、覆盖率、均值 RGB。按帧报在 `analysis`（在色彩转换**之前**的捕获上测）
  - `contactSheet?: { columns?: integer, thumbWidth?: integer(16–2048，默认 480，不放大),
    outPath?: string（默认 `<outPath stem>_sheet.png`） }` — 把所有帧拼成一张带标注（`#index` + 时间）
    的 PNG；传 `{}` 用默认值
- 色彩管线注意：色彩管理工程里通过临时 OCIO Display Transform 调整层实现；无法使用时
  （只读模式、AE 缺该效果、捕获标定失败）回退到纯数学 ACES 转换或原始值并给显式 `colorWarning`。
  **检查响应里的 `colorPipeline` / `colorWarning`。**

## ae_save_project

- 注解：`destructiveHint: true`
- 参数：`path?: string` — 另存为的绝对路径；省略则保存到现有路径（工程从未存过盘会报错）。
- **写盘不可撤销。**

## ae_project_export_json

- 注解：`destructiveHint: false`
- 参数：
  - `outPath?: string` — 写到该绝对路径；省略则**内联**返回（可能很大）
  - `pretty?: boolean` — 2 空格缩进；写盘时默认 `true`，否则默认 `false`
- 覆盖范围：文件夹、合成、图层、关键帧、效果、形状、标记、时间重映射、固态、文件引用。

## ae_project_import_json

- 注解：`destructiveHint: true`
- 参数：
  - `inPath?: string` — `ae_project_export_json` 产出的 JSON 绝对路径；与 `json` 互斥
  - `json?: object` — 内联 JSON 文档（对象，不是字符串）；与 `inPath` 互斥
  - `clearFirst?: boolean` — 导入前清空当前工程的全部条目，默认 `false`（追加）
  - `dryRun?: boolean` — 只校验并返回计划，不碰 AE；适合排查畸形导出
  - `skipValidation?: boolean` — 跳过 Node 侧 schema 校验；只在信任输入、想把坏数据交给 AE 诊断时用

---

## 服务端不提供的能力

- `resources/list` → `-32601 Method not found`
- `prompts/list` → `-32601 Method not found`
- `initialize` 返回的 `instructions` 为空字符串
- `capabilities` 只有 `{ tools: { listChanged: true } }`

## 服务端 stderr 特征行（可用作自检）

```
[mcp-aftereffects] policy: readonly=off, categories=all, eval.run=disabled
[mcp-aftereffects] mailbox: <per-user-temp>/mcp-aftereffects/runtime
[mcp-aftereffects] instance: none registered yet — calls launch AfterFX.exe -r into the running After Effects
[mcp-aftereffects] WRITE ACCESS IS ON — tools can create, mutate and delete project content. Set AE_MCP_READONLY=1 for inspection-only sessions.
```
