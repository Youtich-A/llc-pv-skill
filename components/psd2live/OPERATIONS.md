# PSD2Live：按需接入参考

官方来源：[仓库](https://github.com/tsunehimatoi/psd2live)、[Releases](https://github.com/tsunehimatoi/psd2live/releases)、[文档目录](https://github.com/tsunehimatoi/psd2live/tree/master/docs)。本包仅提供原创操作方法，不携带上游程序、源码或 MCP 代理。上游许可 GPL-3.0，以所下载版本的 LICENSE 为准；本技能 MIT 不覆盖该软件。

## 获取与接入

必须先按 [L2D 路线](../../references/l2d_workflow.md)取得用户肯定，已有授权不重复问。先检查已安装版本和可用工具。缺失时下载匹配系统的官方 Release，或 clone 官方源码后按其构建说明部署；记录具体版本与取得方式。使用接收者选择的工具目录，不能复用开发者机器路径。

在应用内按当前说明启用本地 MCP，优先使用宿主支持的直接连接。只有兼容性需要时才使用所下载版本自带的 `mcp_proxy.py`。绑定回环地址，认证信息只存本地；不要把 bearer token、实际端口配置、用户模型写进技能文件或公开日志。不要覆盖整份客户端配置。

## 从实际 schema 开始

以下名称来自一次 3.6.7 实测，只用于帮助定位，不能代替当前工具发现：

|任务|参考操作|
|---|---|
|上下文/对象/工具定义|`workspace_overview`、`workspace_inspect`、`workspace_list_operations`、`workspace_get_operation`|
|导入与分类|`project_import_psd`、`layer_classify`、`rig_generate`|
|父级与绘制顺序|`rig_edit_structure`|
|参数/关键形/形变|`parameter_update`、`keyform_apply`、`rig_deform`|
|像素与网格|`layer_get_texture`、`layer_replace_image`、`layer_mesh_rebuild`|
|拆分|`source_split_polygon`、`source_split_components`|
|预览渲染|`view_render_model`|
|保存/重新打开|`project_save_as`、`project_save`；打开操作从当前工具列表发现|
|导出|`project_export_psd`、`project_export_model` / `project_export_target`|

先确认目标项目 ID、画布、图层与未保存状态。查询操作的 schema 再写请求，不猜参数名；3.6.7 的 `workspace_get_operation` 使用 `id`。写入通常需要当前 `state`、`project_id`、唯一 `request_id`，以实际接口为准。状态冲突先重读，不盲重放；后台作业等待终态后确认 `applied`/结果，再继续依赖步骤。

`settings_update` 的 `seeThroughEyes` / `seeThroughBrows` 控制五官穿透，是否关闭取决于目标画面；更改生成设置后按接口要求重新生成并复核。脖子的语义角色应是 `neck`，不能只把名字改为 neck 仍维持 face 分类。

3.6.7 一次实测中，`workspace_inspect(scope=settings)` 有结果 schema 不匹配，而 `settings_update` 能正常执行。遇到版本不匹配保留证据，查官方 schema/源码或换受支持路径；不能把局部读取失败当成整个连接失败，也不能因此假定写入成功。拆分产生的 materialized 网格可能拒绝替图并重建，遇此错误先保存并回到可编辑分件源，不叠加不确定修复。

## 渲染与保存

3.6.7 的原生姿态渲染示例（确认当前 schema 后才使用）：

```json
{
  "viewport": {"mode": "canvas_rect", "left": 0, "top": 0, "width": 1024, "height": 1536},
  "target_long_edge": 1536,
  "background": "checkerboard",
  "parameters": {"ParamEyeLOpen": 0, "ParamEyeROpen": 0}
}
```

宽高和参数范围必须从当前模型获取。参数示例不代表所有模型都存在同名参数。渲染响应含图像时保存并实际查看；棋盘格若被渲染进预览图，不能拿该预览图充当透明素材。透明导出另查 Alpha。

操作当前工程时先存副本；导入被未保存状态阻止时，保存当前授权工作再继续，不自动丢弃。交付前保存原生工程并实际重新打开，确认纹理、父级和参数保持；记录应用版本和打开方法。外部模型格式的导出能力与实际兼容测试分别报告。
