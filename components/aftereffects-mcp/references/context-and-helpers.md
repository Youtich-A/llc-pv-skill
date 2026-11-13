
# ae_context 原文摘录（helper / ES3 / tips / undo）

来源：0.3.1接口参考快照，当前行为以真实ae_context为准。建议保持`eval.run`禁用，
下面的 `AE.*` 是服务端 JSX 侧的内部能力，仅在现成原子操作覆盖不到时才考虑。

## helpers —— `AE.*` 可用函数

```
AE.findCompByNameOrId(nameOrId)
AE.findComps(nameOrIdOrPattern)                     — '*' glob supported
AE.findItemById(id)
AE.findItem(idOrName)                               — any project item
AE.findFolder(idOrName)                             — null/undefined = root folder
AE.findLayerInComp(comp, indexOrNameOrIdRef)        — accepts { id: n } (stable Layer.id, AE 22+)
AE.findLayerById(comp, id)
AE.resolveLayers(comp, target)                      — index | name | { id: n } | 'selected' | 'all' | array of those
AE.snapshotKeys(prop) / AE.applyKeys(prop, keys) / AE.removeAllKeys(prop)
AE.setEase(prop, keyIndex, inInf, outInf, inSpeed?, outSpeed?)   — dims/spatial handled
AE.writeValue(prop, value, time?) / AE.readValue(prop, time?)    — separated-dimension safe, __kind values accepted
AE.offsetValue(prop, delta)                         — shift a value or every keyframe
AE.applyKeySpecs(prop, [{time, value, interp?}], {replace, interp, spatialTangents})  — keyframe.apply's engine
AE.moveAnchor(layer, [x, y])                        — anchor move with position compensation
AE.layerRect(layer, time) / AE.pointInRect(rect, preset)         — anchor presets on rendered bounds
AE.shapeGroupBounds(group, {time, includeStroke}) / AE.shapeLayerBounds(layer, opts)
AE.walkShapeContents(contents, fn) / AE.recolorContents(contents, opts) / AE.canonicalGroup(group, precision)
AE.geometryShape('ellipse'|'rect', center, size, roundness)      — a Shape for masks/paths
AE.propertyAtPath(root, path)                       — null instead of throwing
AE.ownerLayer(prop)                                 — the layer a property belongs to
AE.bakeKeysAtTime(root, time)                       — freeze every animated property below root
AE.layerIdSnapshot(comp) / AE.layersSince(comp, snap)            — which layers a command created
AE.withSelection(comp, layers, fn)                  — run a menu command on exactly these layers, selection restored
AE.rect(shapeLayerOrGroup, [w,h], [x,y], {name, roundness, fill:[r,g,b], stroke, strokeWidth})
AE.ellipse(shapeLayerOrGroup, [w,h], [x,y], {name, fill, stroke, strokeWidth})
AE.ensureParentDir(path)                            — mkdir -p for an output file, returns the File
AE.itemTypeName(item)                               — 'CompItem' | 'FootageItem' | 'FolderItem' | 'UnknownItem'
AE.serializeItemSummary(item)
AE.serializeLayerSummary(layer)
AE.serializeLayerFull(layer, opts)                  — opts.detail:'summary' drops default-value props
AE.serializeTransform(layer)
AE.serializePropertyGroup(group, depth, maxDepth, opts)
AE.serializeCompMarkers(comp)
AE.exportProject()
AE.importProject(doc, opts)
AE.safeGet(fn, fallback)
AE.valueToJson(val)
```

## es3Rules —— ExtendScript 语法约束

```
var only (no let/const)
function() {} only (no arrow =>)
string concat only (no template literals)
for(var i=0;i<n;i++) only (no for-of, no forEach/map/filter)
indexOf !== -1 (no includes/startsWith/endsWith)
NEVER chain ternaries: a ? b : c ? d : e parses LEFT-associative in ExtendScript — parenthesize or use if/else
log('msg') to push breadcrumbs
return <JSON-serializable> at end
```

## tips —— 服务端给的实操提示

- 给**已打关键帧**的图层重设父级：用 `layer.set_parent` 且 `jump: true`（不做变换补偿）——
  直接重设父级会改写数值并破坏关键帧。
- 缓动：`keyframe.set_easing`（op）或 `AE.setEase`（eval）—— 两者都处理
  `spatial=1` / 逐维度 `KeyframeEase` 的簿记。
- 审计合成：`ae_layer_info` 用 `layerIndex:'all'` + `detail:'summary'`，跳过默认值属性并保留
  关键帧缓动的 speed/influence。
- 渲染队列的输出文件夹在 `render.add_to_queue` / `render.set_output` / `render.start` 时**自动创建**。
- 一次打很多关键帧：`keyframe.apply` 接受整份列表并可逐键给缓动；它的 `hold` 只持 **OUT** 侧，
  所以“以 hold 键结尾的淡入”仍然会淡入。
- Position 被 Separate Dimensions 拆开（或图层来自 “Create Shapes from Vector Layer”）时，
  每个写操作与 `AE.writeValue` 都会自动路由到跟随属性。
- 导入的 Illustrator 图层：先 `layer.convert_to_shapes`（会剥掉 “ Outlines”，**可能删掉源图层/素材**）；
  再用 `shape.group_bounds` / `layer.split_groups` 逐部件处理。
- 凡是接受 `'all'` 的图层目标都接受数组：`["A", "B", { id: 12 }]` 一次调用。
- 校验运动：`ae_render_frame` 用 `times` + `contactSheet` 把多帧拼成一张带标注的 PNG；
  `analyze` 报边缘色带 / 内容包围盒；`comp.sample` 在多个时间点读数值。
- 多实例（`AfterFX.exe -m`）：每个 MCP server 只寻址**一个**实例，由 `AE_MCP_INSTANCE`
  （实例 id 或它打开的项目文件名）决定；响应里的 `instances[]` 列出谁活着 —— 要改的工程开在别处时，
  **直说**，不要改错实例。

## undoContract —— undo 契约原文

```
every ae_do / eval.run call is auto-wrapped in ONE undo group
one Ctrl+Z (or project.undo) reverts the entire call; batch.run = one call = one undo step
NEVER call app.beginUndoGroup/endUndoGroup in eval.run code — an unbalanced group corrupts undo for the session
undo/redo itself runs OUTSIDE the group: use project.undo (or command.execute 16/2035) as its own call —
  never inside batch.run, and never via eval.run
ae_save_project and files written to disk (rendered PNGs, exported JSON) are NOT undoable
```

## 空工程时的ae_context结构示例（不是连接通过证据）

```json
{
  "ok": true,
  "result": {
    "project": { "file": null, "dirty": true, "numItems": 0, "bitsPerChannel": 8 },
    "instance": null,
    "activeComp": null,
    "selectedLayers": [],
    "items": [],
    "transport": { "mode": "push" },
    "instances": []
  },
  "logs": [],
  "durationMs": 184
}
```

空工程或未登记实例不能证明目标工程连接成功。核对当前实例、工程身份与实际读取；不要把响应耗时或示例值当健康判据。
