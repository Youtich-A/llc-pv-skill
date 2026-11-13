
# ae_do 操作全清单（218 个 / 25 类）

来源：`ae_catalog {}` 实测输出（服务端 0.3.1，策略 `readonly=off, categories=all, eval.run=disabled`）。
本文件只列**操作名**。**每个操作的确切参数必须用 `ae_catalog {category}` 现查**——
服务端会按声明做校验，缺参/类型错/多余键在接触 AE 之前就被拒绝。

## batch（1）

- `batch.run`

## command（3）

- `command.execute`
- `command.find`
- `command.list`

## comp（17）

- `comp.create`
- `comp.set_label`
- `comp.set_props`
- `comp.set_renderer`
- `comp.list_renderers`
- `comp.set_work_area`
- `comp.add_guide`
- `comp.remove_guide`
- `comp.set_guide`
- `comp.list_guides`
- `comp.delete`
- `comp.precompose`
- `comp.duplicate`
- `comp.info`
- `comp.set_layer_order`
- `comp.resize`
- `comp.sample`

## effect（7）

- `effect.add`
- `effect.remove`
- `effect.list_on_layer`
- `effect.set_property`
- `effect.move`
- `effect.set_dropdown_items`
- `effect.get_dropdown_items`

## egp（7）— Essential Graphics 面板 / 动态图形模板

- `egp.set_name`
- `egp.add_property`
- `egp.list_controllers`
- `egp.export_mogrt`
- `egp.set_alternate_source`
- `egp.add_layer`
- `egp.open_in_panel`

## expression（4）

- `expression.set`
- `expression.disable_all`
- `expression.restore_all`
- `expression.remove`

## font（11）

- `font.list`
- `font.list_missing`
- `font.info`
- `font.check_glyphs`
- `font.list_used`
- `font.list_duplicates`
- `font.get_lists`
- `font.set_favorites`
- `font.set_substitution`
- `font.get_default_for_script`
- `font.set_default_for_script`

## footage（7）

- `footage.replace`
- `footage.interpret`
- `footage.reload`
- `footage.list_missing`
- `footage.replace_with_solid`
- `footage.replace_with_placeholder`
- `footage.set_proxy`

## instance（5）

- `instance.list`
- `instance.start`
- `instance.stop`
- `instance.dialogs`
- `instance.dismiss_dialog`

## item（5）

- `folder.create`
- `item.move_to_folder`
- `item.set_props`
- `item.list`
- `item.usages`

## keyframe（13）

- `keyframe.add`
- `keyframe.apply`
- `keyframe.remove`
- `keyframe.set_easing`
- `keyframe.set_batch`
- `keyframe.shift`
- `keyframe.copy`
- `keyframe.set_spatial`
- `keyframe.set_roving`
- `keyframe.set_value`
- `keyframe.set_interpolation`
- `keyframe.set_label`
- `keyframe.set_selected`

## layer（36）

- `layer.create_solid`
- `layer.create_adjustment`
- `layer.create_shape`
- `layer.create_text`
- `layer.create_null`
- `layer.create_camera`
- `layer.create_light`
- `layer.create_parametric_mesh`
- `layer.delete`
- `layer.duplicate`
- `layer.set_parent`
- `layer.scene_edit_detection`
- `layer.move`
- `layer.create_footage`
- `layer.set_enabled`
- `layer.set_guide`
- `layer.set_props`
- `layer.add_guide`
- `layer.remove_guide`
- `layer.move_guide`
- `layer.list_guides`
- `layer.bounds`
- `layer.convert_point`
- `layer.apply_preset`
- `layer.replace_source`
- `layer.set_track_matte`
- `layer.set_blend_mode`
- `layer.split`
- `layer.copy_to_comp`
- `layer.calculate_transform`
- `layer.info`
- `layer.split_groups`
- `layer.convert_to_shapes`
- `layer.set_anchor`
- `layer.set_timing`
- `layer.set_visibility_schedule`

## marker（5）

- `marker.add_comp`
- `marker.add_layer`
- `marker.remove`
- `marker.update`
- `marker.list`

## mask（4）

- `mask.add`
- `mask.set_path`
- `mask.set_props`
- `mask.remove`

## pref（5）— 首选项

- `pref.get`
- `pref.set`
- `pref.delete`
- `pref.get_setting`
- `pref.set_setting`

## project（27）

- `project.open`
- `project.import_file`
- `project.undo`
- `project.purge`
- `project.replace_font`
- `project.auto_fix_expressions`
- `project.clear`
- `project.delete_item`
- `project.find_layers`
- `project.list_effects`
- `project.set_settings`
- `project.get_settings`
- `project.reduce`
- `project.remove_unused_footage`
- `project.consolidate_footage`
- `project.import_placeholder`
- `project.new`
- `project.parse_swatch`
- `project.get_xmp`
- `project.set_xmp`
- `project.set_default_import_folder`
- `project.get_tool`
- `project.set_tool`
- `project.set_memory_limits`
- `project.set_multi_frame_rendering`
- `project.merge`
- `project.rename`

## property（8）

- `property.set`
- `property.get`
- `property.list`
- `property.add`
- `property.remove`
- `property.separate_dimensions`
- `property.move`
- `property.select`

## render（15）

- `render.add_to_queue`
- `render.start`
- `render.clear_queue`
- `render.set_output`
- `render.get_settings`
- `render.set_settings`
- `render.set_om_settings`
- `render.remove_item`
- `render.duplicate_item`
- `render.list_templates`
- `render.status`
- `render.queue_in_ame`
- `render.variants`
- `render.save_template`
- `render.frame`

## shape（22）

- `shape.add_group`
- `shape.add_rect`
- `shape.add_ellipse`
- `shape.add_fill`
- `shape.add_path`
- `shape.add_trim_paths`
- `shape.add_merge_paths`
- `shape.add_stroke`
- `shape.add_polystar`
- `shape.add_repeater`
- `shape.add_rounded_corners`
- `shape.add_offset_paths`
- `shape.add_wiggle_paths`
- `shape.add_zigzag`
- `shape.add_pucker_bloat`
- `shape.add_twist`
- `shape.add_gradient_fill`
- `shape.add_gradient_stroke`
- `shape.add_wiggle_transform`
- `shape.group_bounds`
- `shape.recolor`
- `shape.signature`

## text（10）

- `text.set_content`
- `text.set_style`
- `text.set_style_range`
- `text.measure`
- `text.set_box`
- `text.set_variable_font`
- `text.add_font_axis`
- `text.add_animator`
- `text.paste_range`
- `text.reset_style`

## timeline（3）

- `timeline.set_time`
- `timeline.set_active_comp`
- `timeline.select_layers`

## transform（1）

- `transform.set`

## viewer（2）

- `viewer.get_state`
- `viewer.set_options`

---

## 服务端 `undo` 字段原文

> every ae_do call runs in ONE automatic undo group — a single Ctrl+Z / project.undo reverts the whole call
> (batch.run included); never open an undo group yourself. undo/redo itself (project.undo,
> command.execute 16/2035) is the exception: it runs outside the group, so call it alone, never inside batch.run
