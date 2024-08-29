import bpy
import bmesh
import re

# ASSUMES CURSOR IS IN BOTTOM RIGHT OF UV

# Save the original area type to switch back later
original_area = bpy.context.area.type

pattern = re.compile(r".*Part 1\..*")


# Get all mesh objects in the scene
mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and pattern.match(obj.name)]

# Iterate over all mesh objects
for ob in mesh_objects:
    bpy.context.view_layer.objects.active = ob
    bpy.context.view_layer.update()
    
    # Switch to Edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Create a BMesh from the object
    bm = bmesh.from_edit_mesh(ob.data)
    
    # Move to UV Editor
    bpy.context.area.ui_type = 'UV'
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Ensure UV sync selection is enabled
    bpy.context.scene.tool_settings.use_uv_select_sync = True
    
    # Select all UVs
    bpy.ops.uv.select_all(action='SELECT')
    
    # Move all UVs by x -1
    bpy.ops.transform.translate(value=(-1, 0, 0), constraint_axis=(True, False, False))
    
    # Clear selection
    bpy.ops.uv.select_all(action='DESELECT')
    
    # Switch back to the original area type
    bpy.context.area.ui_type = original_area
    
    # Switch to Edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select vertices with x < 0
    for v in bm.verts:
        v.select = v.co.x < -0.001
    
    # Expand the selection
    bpy.ops.mesh.select_more()
    
    # Update the BMesh
    bmesh.update_edit_mesh(ob.data)
    
    # Switch to UV Editor mode
    bpy.context.area.ui_type = 'UV'
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Ensure UV sync selection is enabled
    bpy.context.scene.tool_settings.use_uv_select_sync = True
    
    # Set the pivot to 2D cursor
    bpy.context.space_data.pivot_point = 'CURSOR'
    
    # Scale UVs by -1 along the X axis
    bpy.ops.transform.resize(value=(-1, 1, 1), orient_type='GLOBAL', mirror=True, use_proportional_edit=False)
    
    # Select all UVs
    bpy.ops.uv.select_all(action='SELECT')
    
    # Scale UVs by 0.5 along the X axis
    bpy.ops.transform.resize(value=(0.5, 1, 1), orient_type='GLOBAL', mirror=True, use_proportional_edit=False)
    
    # Move UVs by 0.5 along the X axis
    bpy.ops.transform.translate(value=(0.5, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL')
    
    # Switch back to the original area type
    bpy.context.area.ui_type = original_area
    bpy.ops.object.mode_set(mode='OBJECT')

# Restore the original area type
bpy.context.area.type = original_area
