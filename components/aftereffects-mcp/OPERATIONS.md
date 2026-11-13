# AE MCP便携操作说明

本组件迁移连接知识和操作参考，删除了原机器配置。以@kumoproductions/mcp-aftereffects 0.3.1接口为参考；0.3.2为新接入示例版本。当前工具schema、ae_catalog和ae_context才是执行依据，操作数量不是兼容保证。

先完成[环境检查](../../references/ae_environment.md)，再按需读：[工具参数](references/tools.md)、[操作索引](references/operations.md)、[ES3与helpers](references/context-and-helpers.md)。这些为参考快照，不能覆盖当前真实响应。

## 工作循环

`工具发现 → ae_context / ae_version_info → 确认工程与实例 → ae_catalog查询类别 → ae_do原子操作 → ae_render_frame多帧 → 查看PNG → 修正和回归`。

- 多项相关且可一起回退的操作适合batch.run。实例启停等特殊操作是否可批处理，以当前目录声明为准；不把所有操作强塞一个大batch。
- 默认先用summary和includeProperties=false等最小读取；需要某属性再加载局部，不拉全项目完整JSON来增加上下文。
- 同名合成、重复字与重复角色实例用稳定ID/明确上下文定位，不能只依赖显示名。
- 渲染多时间点覆盖入场、中间、完成态与退出；contactSheet和analyze辅助检查，不代替视觉判断。检查colorPipeline和colorWarning，不能把原始工作空间值截图当显示色。

## Undo与文件

ae_do自动维护撤销组，不自行嵌套beginUndoGroup/endUndoGroup。undo/redo独立调用，不混进batch。保存工程、导出JSON和PNG写盘不能依靠Ctrl+Z撤回。工程先确认目标与工作副本，清空/覆盖必须在任务明确授权范围内。

## 高频问题

- 属性路径从真实图层信息获取；不要猜本地化显示名。新增indexed属性后重新取引用。
- 重设父级先确定保留世界姿态还是局部值，核对补偿与已有关键帧；jump参数以目录语义和多帧结果验证，不能一律开启。
- Position分离维度、文本颜色RGB/RGBA、hold只影响哪一侧等按真实属性/接口验证。不要用同一颜色数组或缓动规则覆盖所有属性。
- JSX若确有必要，只能使用宿主支持的ES3语法。helpers是服务端内部接口，不是可以直接从客户端调用的独立MCP工具。默认不启用eval.run。
- 渲染输出模板按当前AE枚举，不能照抄旧机器的模板名称。已完成队列项不要按待渲染项写属性。
- 多实例先核实目标，不自动切工程、关闭实例或合并未保存内容。

## 不适用

未暴露MCP工具时，不宣称已经连上AE。不得用ae_do代替本机shell/文件系统工具。AE安装、账户、字体、插件许可由使用者环境提供，本组件不包含Adobe软件或授权。
