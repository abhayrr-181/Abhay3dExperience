import bpy
import math

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create board
bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 0.1))
board = bpy.context.active_object
board.name = 'Board'
board.scale = (2, 0.3, 0.05)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=10)
bpy.ops.object.mode_set(mode='OBJECT')

# Create mast
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=3, enter_editmode=False, align='WORLD', location=(0, 0, 1.5), scale=(1, 1, 1))
mast = bpy.context.active_object
mast.name = 'Mast'
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=10)
bpy.ops.object.mode_set(mode='OBJECT')

# Create boom
bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=2, enter_editmode=False, align='WORLD', location=(1, 0, 1.2), scale=(1, 1, 1))
boom = bpy.context.active_object
boom.name = 'Boom'
boom.rotation_euler = (0, math.pi/2, 0)

# Create foot straps
bpy.ops.mesh.primitive_cube_add(size=0.1, enter_editmode=False, align='WORLD', location=(0.5, 0, 0.06), scale=(1, 0.5, 0.02))
strap1 = bpy.context.active_object
strap1.name = 'FootStrap1'

bpy.ops.mesh.primitive_cube_add(size=0.1, enter_editmode=False, align='WORLD', location=(-0.5, 0, 0.06), scale=(1, 0.5, 0.02))
strap2 = bpy.context.active_object
strap2.name = 'FootStrap2'

# Create fin
bpy.ops.mesh.primitive_cone_add(radius1=0.1, radius2=0.05, depth=0.2, enter_editmode=False, align='WORLD', location=(0, -0.3, -0.1), scale=(1, 1, 1))
fin = bpy.context.active_object
fin.name = 'Fin'
fin.rotation_euler = (math.pi, 0, 0)

# Create sail
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0.5, 0, 1.5), scale=(1, 1, 1))
sail = bpy.context.active_object
sail.name = 'Sail'
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=20)
bpy.ops.object.mode_set(mode='OBJECT')

# Create rope (optional)
bpy.ops.mesh.primitive_cylinder_add(radius=0.005, depth=2, enter_editmode=False, align='WORLD', location=(0.5, 0, 1.5), scale=(1, 1, 1))
rope = bpy.context.active_object
rope.name = 'Rope'
rope.rotation_euler = (0, math.pi/2, 0)

# Set up armature for board
bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
armature_board = bpy.context.active_object
armature_board.name = 'Armature_Board'
bpy.ops.object.mode_set(mode='EDIT')
bone = armature_board.data.edit_bones.new('Board_Bone')
bone.head = (0, 0, 0)
bone.tail = (0, 0, 0.1)
bpy.ops.object.mode_set(mode='OBJECT')

# Parent board to armature
board.select_set(True)
armature_board.select_set(True)
bpy.context.view_layer.objects.active = armature_board
bpy.ops.object.parent_set(type='ARMATURE')

# Set up armature for sail
bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0.5, 0, 1.5), scale=(1, 1, 1))
armature_sail = bpy.context.active_object
armature_sail.name = 'Armature_Sail'
bpy.ops.object.mode_set(mode='EDIT')
for i in range(6):
    bone = armature_sail.data.edit_bones.new(f'Sail_Bone_{i}')
    bone.head = (0.5 + i*0.2, 0, 1.5 - i*0.1)
    bone.tail = (0.5 + i*0.2, 0, 1.5 - i*0.1 + 0.1)
bpy.ops.object.mode_set(mode='OBJECT')

# Parent sail to armature
sail.select_set(True)
armature_sail.select_set(True)
bpy.context.view_layer.objects.active = armature_sail
bpy.ops.object.parent_set(type='ARMATURE')

# Set up materials
def create_material(name, base_color=(1,1,1,1), roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    return mat

board_mat = create_material('Board_Mat', base_color=(0.8, 0.8, 0.8, 1), roughness=0.3, metallic=0.1)
mast_mat = create_material('Mast_Mat', base_color=(0.9, 0.9, 0.9, 1), roughness=0.2, metallic=0.0)
boom_mat = create_material('Boom_Mat', base_color=(0.7, 0.7, 0.7, 1), roughness=0.4, metallic=0.0)
sail_mat = create_material('Sail_Mat', base_color=(1, 1, 1, 0.8), roughness=0.1, metallic=0.0)
sail_mat.blend_method = 'BLEND'

board.data.materials.append(board_mat)
mast.data.materials.append(mast_mat)
boom.data.materials.append(boom_mat)
sail.data.materials.append(sail_mat)
strap1.data.materials.append(board_mat)
strap2.data.materials.append(board_mat)
fin.data.materials.append(board_mat)
rope.data.materials.append(mast_mat)

# Set up animation
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 150  # 5 seconds at 30fps

# Animate board rocking
armature_board.animation_data_create()
action = bpy.data.actions.new("Board_Action")
armature_board.animation_data.action = action

# Pitch and roll
for frame in range(1, 151):
    angle = math.sin(frame * 0.1) * 0.05  # Small angle
    armature_board.pose.bones['Board_Bone'].rotation_euler = (angle, 0, angle)
    armature_board.pose.bones['Board_Bone'].keyframe_insert(data_path="rotation_euler", frame=frame)

# Animate sail flapping
armature_sail.animation_data_create()
action_sail = bpy.data.actions.new("Sail_Action")
armature_sail.animation_data.action = action_sail

for bone_name in [f'Sail_Bone_{i}' for i in range(6)]:
    for frame in range(1, 151):
        angle = math.sin(frame * 0.2 + i*0.5) * 0.1  # Variations
        armature_sail.pose.bones[bone_name].rotation_euler = (0, angle, 0)
        armature_sail.pose.bones[bone_name].keyframe_insert(data_path="rotation_euler", frame=frame)

# Calculate total polycount
total_tris = 0
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        total_tris += len(obj.data.polygons)
print(f"Total polycount: {total_tris} tris")

# Export to GLB
bpy.ops.export_scene.gltf(filepath='windsurf_model.glb', export_format='GLB', export_animations=True, export_apply=True, export_yup=True)
