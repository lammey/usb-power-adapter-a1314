# Scrapbook 

- https://all3dp.com/2/blender-to-3d-printer-prepare-model/
- https://www.sculpteo.com/en/3d-learning-hub/create-3d-file/fix-non-manifold-geometry/
- https://blender.stackexchange.com/questions/45004/how-to-make-boolean-modifiers-with-python
- https://blender.stackexchange.com/questions/34781/the-boolean-modifier-is-not-working

```
bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.ops.transform.resize(value=(13.2796, 13.2796, 13.2796), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.translate(value=(-0, -0, -12.2828), orient_axis_ortho='X', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.context.space_data.context = 'MODIFIER'
bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles()
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.modifier_apply(modifier="Boolean")
bpy.ops.outliner.delete(hierarchy=True)


```

- `bpy.context.view_layer.objects.active = obj` select object
- `bpy.ops.object.select_all(action='DESELECT')` deselect all
- `for obj in bpy.context.selected_objects:` iterate through objects in selection

- We need to create thread, core as separate objects so we can intersect thread with cube.
    - Rather than do that, easier to bisect with a plane somehow?
- We can combine thread and core with a boolean modifier on the core I believe.
    - This avoids the trouble of creating faces inbetween the thread loops
- Then we need to run remove doubles, as the boolean modifier messes with the geometry
    - This seems to require being in edit mode, which itself requires an active object.