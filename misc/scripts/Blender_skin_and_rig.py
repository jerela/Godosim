import bpy, bmesh
import json
import mathutils
import math


def get_connector_bone_name(parent_name, bone_name):
    return 'connector_from_' + parent_name + '_to_' + bone_name





def run(skel_variant):

    # 1: LOAD DATA AND DEFINE SETTINGS
    # whether to create bones that connect bodies that are not automatically connected (e.g., femur_r and pelvis, where femur_r begins in a different place than pelvis ends)
    create_connecting_bones = True
    connecting_bones_can_deform = True

    # whether to create a Godot-compliant armature
    upwards_bones_only = True

    # deforming bones: bones that are allowed to deform the skin mesh
    # Gait2354
    #deforming_bones = ['femur_r', 'femur_l', 'tibia_r', 'tibia_l', 'calcn_r', 'calcn_l', 'pelvis', 'torso']
    # BSM
    #deforming_bones = ['femur_r', 'femur_l', 'tibia_r', 'tibia_l', 'calcn_r', 'calcn_l', 'pelvis', 'lumbar_body', 'thorax', 'head', 'scapula_r', 'scapula_l', 'humerus_r', 'humerus_l', 'radius_r', 'radius_l', 'hand_r', 'hand_l']
    # Hamner-Godosim
    deforming_bones = ['femur_r', 'femur_l', 'tibia_r', 'tibia_l', 'talus_r', 'talus_l', 'calcn_r', 'calcn_l', 'pelvis', 'torso', 'humerus_r', 'humerus_l', 'radius_r', 'radius_l', 'ulna_r', 'ulna_l', 'hand_r', 'hand_l']


    # open the files for hierarchy and bone endpoints in the global coordinate frame
    f = open(r'C:\Users\JohnDoe\Documents\Godosim-assets\matlab_outputs\hierarchy.json', 'r')
    # get the json object as a dict 
    hierarchy = json.load(f)
    f.close()

    f = open(r'C:\Users\JohnDoe\Documents\Godosim-assets\matlab_outputs\bone_endpoints_' + skel_variant + '.json', 'r')
    # get the json object as a dict 
    bone_endpoints = json.load(f)
    f.close()

    f = open(r'C:\Users\JohnDoe\Documents\Godosim-assets\matlab_outputs\bone_rotations_' + skel_variant + '.json', 'r')
    # get the json object as a dict 
    bone_rotations = json.load(f)
    f.close()

    f = open(r'C:\Users\JohnDoe\Documents\Godosim-assets\matlab_outputs\generalized_coordinates_' + skel_variant + '.json', 'r')
    # get the json object as a dict 
    generalized_coordinates = json.load(f)
    f.close()


    # get the numbers of bones in the read data
    n_endpoints = len(bone_endpoints)
    n_bones = n_endpoints

    # loop through the names of bones and print them
    bone_names = []
    keys = list(bone_endpoints)
    for i in range(n_bones):
        bone_names.append(keys[i])


    print('Bone names: ', bone_names)


    # 2: CREATE ARMATURE

    my_armature = bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    arm_obj = bpy.data.objects['Armature']
    # must be in edit mode to add bones
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    edit_bones = arm_obj.data.edit_bones

    # remove Blender's default-constructed bones, if Blender created any
    for bone in edit_bones:
        arm_obj.data.edit_bones.remove(bone)


    tail_offset = [0, 0.2, 0]
    #print('tail offset: ', tail_offset)

    # loop through bones to set their head and tail coordinates
    for i in range(len(bone_names)):
        bone_name = bone_names[i]
        
        # get the head and tail of the body
        body_head = bone_endpoints[bone_name]['head']
        body_tail = bone_endpoints[bone_name]['tail']
        
        # create the base upwards bone
        b = edit_bones.new(bone_name)
        b.head = body_head
        # If bone isn't for Ground, we rotate Blender armature bones that are used in Godosim to apply transforms from the OpenSim model. This is done because the OpenSim model's default pose has the bodies in non-zero rotations, so we must apply the appropriate rotations in the Blender armature as well.
        if bone_name != 'ground':
            # we get the 9-element vector of 3x3 rotation matrix elements for the current bone
            mat_elems = bone_rotations[bone_name]
            # then we construct a Blender rotation matrix using the elements
            seq = (mat_elems[0:3], mat_elems[3:6], mat_elems[6:9])
            mat = mathutils.Matrix(seq)
            # we then wrap tail_offset in a Blender vector to enable matrix multiplication
            vec = mathutils.Vector(tail_offset)
            # Perform matrix multiplication and set tail_final as the rotated tail
            tail_final = mat@vec
        else:
            # otherwise, tail_final is the original tail (for Ground)
            tail_final = tail_offset
        
        #rotated_tail = tail_offset
        b.tail = [body_head[0]+tail_final[0], body_head[1]+tail_final[1], body_head[2]+tail_final[2]]
        arm_obj.data.edit_bones[bone_name].use_deform = False
        arm_obj.data.edit_bones[bone_name].use_inherit_rotation = False
        arm_obj.data.edit_bones[bone_name].roll = 0
        
        # create the segment bone that is used for attachment to mesh
        segment_bone_name = bone_name + '_segment'
        b_segment = edit_bones.new(segment_bone_name)
        b_segment.head = body_head
        # if bone has children, we assign its tail normally; if it doesn't have children (e.g., hand), its tail has been set manually to a nonsensical value in the text file, so we want to instead make it reach towards the opposite end of the segment for weight painting to be created accurately
        if bone_name in hierarchy.values():
            b_segment.tail = body_tail
        else:
            b_segment.tail = [body_head[0]-tail_final[0], body_head[1]-tail_final[1], body_head[2]-tail_final[2]]
        # parent the segment bone to the base bone so we can move the segment indirectly by moving the base bone
        arm_obj.data.edit_bones[segment_bone_name].parent = arm_obj.data.edit_bones[bone_name]
        arm_obj.data.edit_bones[segment_bone_name].use_inherit_rotation = True
        
        print('Created bone', bone_name, 'at', b.head, b.tail)
        # if bone has been named in deforming bones, we set a property to allow it to deform the skin mesh
        if bone_name in deforming_bones:
            arm_obj.data.edit_bones[segment_bone_name].use_deform = True
            print(bone_name, 'is allowed to deform')
        else:
            arm_obj.data.edit_bones[segment_bone_name].use_deform = False

    # loop through bones to set their parent bones and connect them to their parents, and possibly to create connecting bones between them
    for i in range(len(bone_names)):
        bone_name = bone_names[i]
        # we skip ground because it has no parent in the OpenSim model
        if bone_name != 'ground':
            # get the head and tail coordinates in Blender coordinate system
            print(bone_name)
            parent_name = hierarchy[hierarchy[bone_name]]
            parent_tail = bone_endpoints[parent_name]['tail']
            child_head = bone_endpoints[bone_name]['head']
            # if the parent bone ends where the child bone begins, we apply parent-child relationship normally
            if parent_tail == child_head:
                print('tail and head match for', parent_name, 'and', bone_name)
                arm_obj.data.edit_bones[bone_name].parent = arm_obj.data.edit_bones[parent_name + '_segment']
                #arm_obj.data.edit_bones[bone_name].use_connect = True
            # otherwise, if the tail of the parent is not located at the head of the child, we can create connecting bones between them
            elif create_connecting_bones:
                print('tail and head mismatch between', parent_name, 'and', bone_name)
                connector_bone_name = get_connector_bone_name(parent_name, bone_name)
                b = edit_bones.new(connector_bone_name)
                b.head = parent_tail
                b.tail = child_head
                arm_obj.data.edit_bones[connector_bone_name].parent = arm_obj.data.edit_bones[parent_name + '_segment']
                # when use_connect is true, the bone's head is stuck to the parent's tail
                arm_obj.data.edit_bones[connector_bone_name].use_connect = True
                arm_obj.data.edit_bones[connector_bone_name].use_deform = connecting_bones_can_deform
                arm_obj.data.edit_bones[bone_name].parent = arm_obj.data.edit_bones[connector_bone_name]
                arm_obj.data.edit_bones[bone_name].use_connect = True
                
            
    # we must rotate the armature such that OpenSim coordinate system is rotated to match that of Blender
    # first rotate such that the vertical axis is z instead of y
    mat_rot_x = mathutils.Matrix.Rotation(math.radians(90), 4, 'X')
    arm_obj.data.transform(mat_rot_x)
    # then rotate 90 degrees clockwise along the vertical axis
    mat_rot_z = mathutils.Matrix.Rotation(math.radians(-90), 4, 'Z')
    arm_obj.data.transform(mat_rot_z)
    # now the armature shows upright in Blender and we can do, e.g., x-axis mirroring when moving bones or symmetric weight painting


    #bpy.context.object.rotation_euler[0] = 1.5708
    #bpy.context.object.rotation_euler[2] = -1.5708
        
    bpy.ops.object.mode_set(mode='OBJECT')

    arm_obj.show_in_front = True


    # hide the bone running from ground to pelvis in all but edit mode
    arm_obj.data.bones['ground'].hide = True


    # exit edit mode to save bones so they can be used in pose mode
    bpy.ops.object.mode_set(mode='OBJECT')




    # 3: IMPORT THE SKIN MESH AND ASSOCIATE IT WITH THE ARMATURE

    # 3.1: IMPORT AND TRANSLATE THE MESH TO MATCH WITH THE ARMATURE

    # import the SKEL skin mesh
    skel_file = 'C:/Users/JohnDoe/Documents/Godosim-assets/skel_outputs/skin_mesh_' + skel_variant + '.obj'
    bpy.ops.wm.obj_import(filepath=skel_file)

    # set the scale of the mesh so that the OpenSim model and the mesh are of equal height
    skin_mesh = bpy.data.objects['skin_mesh_' + skel_variant]
    #opensim_model_height = 1.8
    #scale_factor = opensim_model_height / skin_mesh.dimensions.y
    #bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)

    # read pelvis location from SKEL output file
    #pelvis_skel = [0.0025912, -0.20103,  0.099523]

    bone_names_file = open('C:/Users/JohnDoe/Documents/Godosim-assets/skel_outputs/bone_names.txt', 'r')
    bnames = bone_names_file.readlines()
    bone_names_file.close()

    joint_translations_file = open('C:/Users/JohnDoe/Documents/Godosim-assets/skel_outputs/joint_translations_' + skel_variant + '.txt', 'r')
    lines = joint_translations_file.readlines()
    joint_translations_file.close()

    print(lines[0])
    pelvis_translation = lines[0].split(',')
    print(pelvis_translation)

    pelvis_skel = []
    pelvis_skel.append(float(pelvis_translation[0]))
    pelvis_skel.append(float(pelvis_translation[1]))
    pelvis_skel.append(float(pelvis_translation[2]))

    # align the pelvis of SKEL with the pelvis of the OpenSim-derived armature
    pelvis_head = bone_endpoints['pelvis']['head']

    # when setting the mesh location, we apply the scale factor to the SKEL pelvis positions
    #skin_mesh.location.x = 0*scale_factor
    #skin_mesh.location.y = pelvis_skel[2]*scale_factor
    # in the vertical direction, we add the vertical origin of the pelvis in the OpenSim model to ensure matching between the armature and the mesh
    #skin_mesh.location.z = -pelvis_skel[1]*scale_factor + pelvis_head[1]

    # we need to add the pelvis position in ground and subtract the SKEL offset of pelvis to match the skin mesh with the armature
    #skin_mesh.location.z = 0.94 - float(pelvis_translation[1])

    #skin_mesh.location.x = 0
    #skin_mesh.location.y = 0
    #skin_mesh.location.z = 0.94 - pelvis_skel[1]


    # 3.2: USE AUTOMATIC SKINNING TO GENERATE THE VERTEX GROUPS AND WEIGHTS

    # parent the mesh to the armature with automatic weights
    bpy.ops.object.select_all(action='DESELECT')
    # first select mesh, then armature
    skin_mesh.select_set(True)
    arm_obj.select_set(True)
    # make sure armature is the active object
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    bpy.ops.object.select_all(action='DESELECT') 



    # 3.3: TUNE THE WEIGHTS TO IMPROVE REALISM OF DEFORMATION

    # modify deformation weights in the vertex groups to make deformations more realistic

    vertex_group_targets = dict()
    vertex_group_name_to_idx = dict()
    # create a mapping from vertex group names (e.g., "femur_l_segment") to its index in the vertex groups list
    for g in skin_mesh.vertex_groups:
        vertex_group_name_to_idx[g.name] = g.index
    # create a mapping from a vertex group of a connector bone (e.g., "connector_from_torso_to_humerus_r") to its "parent" bone by index
    for g in skin_mesh.vertex_groups:
        if g.name.startswith("connector_"):
            origin_group = g.name[15:]
            idx = origin_group.find('_to_')
            origin_group = origin_group[:idx]
            origin_group += '_segment'
            vertex_group_targets[g.index] = vertex_group_name_to_idx[origin_group]
               
    # modify vertex groups in a new bmesh instance and assign the results to the original mesh
    bm = bmesh.new()
    bm.from_mesh(skin_mesh.data)

    # only ever one deform weight layer
    dvert_layer = bm.verts.layers.deform.active

    # loop through all vertices and modify their vertex group weights
    for vert in bm.verts:
        dvert = vert[dvert_layer]
        for k in vertex_group_targets.keys():
            if k in dvert:
                target_group = vertex_group_targets[k]
                # if the vertex has the target vertex group, we simply add to its value; otherwise we add that vertex group to the vertex
                if vertex_group_targets[k] in dvert:
                    dvert[target_group] += dvert[k]
                    # finally, we zero the weight in the connector bone's vertex group                
                else:
                    dvert[target_group] = dvert[k]
                # finally, we zero the weight in the connector bone's vertex group
                dvert[k] = 0

                

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(skin_mesh.data)
    bm.free()  # free and prevent further access

    # once we've refined the vertex deformation weights, we can and should remove the vertex groups of connector bones
    for g in skin_mesh.vertex_groups:
        if g.name.startswith("connector_"):
            vg = skin_mesh.vertex_groups.get(g.name)
            skin_mesh.vertex_groups.remove(vg)
    # we also remove the connector bones themselves
    bpy.ops.object.mode_set(mode='EDIT')
    bones_to_remove = []
    for bone in arm_obj.data.edit_bones:
        if bone.name.startswith('connector_'):
            bones_to_remove.append(bone)
    for bone in bones_to_remove:
        print("Removing " + bone.name)
        arm_obj.data.edit_bones.remove(bone)
        
    bpy.ops.object.mode_set(mode='OBJECT')



    # 3.4: ADJUST THE ROLL OF EDITBONES IN UPPER ARMS FOR MORE REALISTIC DEFORMATION
    bpy.ops.object.mode_set(mode='EDIT')

    for bone_name in bone_names:
        if bone_name == 'ground':
            continue

        # this will make the arms, particularly forearms and wrists, deform more realistically by accounting for the axial rotation generalized coordinates in them
        # the factors in front of the values of the generalized coordinates come from the axial component of the rotation axis of the generalized coordinate            
        if bone_name == 'radius_r' or bone_name == 'hand_r':
            roll = 0.99840646*generalized_coordinates['pro_sup_r']
            arm_obj.data.edit_bones[bone_name].roll += roll
            print(bone_name + ' pronation-supination correction: ' + str(math.degrees(roll)))
        if bone_name == 'radius_l' or bone_name == 'hand_l':
            roll = -0.99840646*generalized_coordinates['pro_sup_l']
            arm_obj.data.edit_bones[bone_name].roll += roll
            print(bone_name + ' pronation-supination correction: ' + str(math.degrees(roll)))
        if bone_name == 'radius_r' or bone_name == 'hand_r' or bone_name == 'humerus_r':
            roll = 1.0*generalized_coordinates['arm_rot_r']
            arm_obj.data.edit_bones[bone_name].roll += roll
            print(bone_name + ' arm rotation correction: ' + str(math.degrees(roll)))
        if bone_name == 'radius_l' or bone_name == 'hand_l' or bone_name == 'humerus_l':
            roll = -1.0*generalized_coordinates['arm_rot_l']
            arm_obj.data.edit_bones[bone_name].roll += roll
            print(bone_name + ' arm rotation correction: ' + str(math.degrees(roll)))
        #mat_elems = bone_rotations[bone_name]
        #seq = (mat_elems[0:3], mat_elems[3:6], mat_elems[6:9])
        #mat = mathutils.Matrix(seq)
        #axis_angle = mat.to_quaternion().to_axis_angle()
        #print(bone_name + ' axang would be: ' + str(math.degrees(axis_angle[1])))
    bpy.ops.object.mode_set(mode='OBJECT')


    # 4: PREPARE UV MAPS TO TEXTURES CAN BE PROJECTED ON THE MESH

    # TRANSFER UV MAPS FROM SMPL TO SKEL

    # import the SMPL mesh with a UV map
    smpl_file = 'C:/Users/JohnDoe/Documents/Godosim-assets/smpl-uv/smpl_uv.obj'
    bpy.ops.wm.obj_import(filepath=smpl_file)
    smpl_mesh = bpy.data.objects['smpl_uv']
    # transfer the UV map to skin mesh
    bpy.ops.object.select_all(action='DESELECT')
    skin_mesh.select_set(True)
    smpl_mesh.select_set(True)
    bpy.context.view_layer.objects.active = smpl_mesh
    bpy.ops.object.join_uvs()
    bpy.ops.object.select_all(action='DESELECT') 
    # delete the SMPL mesh as we no longer need it
    smpl_mesh.select_set(True)
    bpy.ops.object.delete(use_global=False, confirm=False)

    bpy.ops.object.select_all(action='DESELECT') 





    # we must set smooth shading to prevent a vertex lighting-like effect and allow more realistic light on the mesh
    skin_mesh.select_set(True)
    bpy.ops.object.shade_smooth()

    # 5: SAVE OUTPUT MODELS

    # save file
    glb_out_file = 'C:/Users/JohnDoe/Documents/Godosim-importables/SMPL_Hamner/human_' + skel_variant + '.glb'
    bpy.ops.export_scene.gltf(filepath=glb_out_file, export_materials='PLACEHOLDER')
    
    

def clear_data():
    # remove all objects
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    # purge orphans like materials and meshes
    bpy.ops.outliner.orphans_purge()


body_morphologies = ['female_zero', 'female_plus1', 'female_plus2', 'female_minus1', 'female_minus2', 'male_zero', 'male_plus1', 'male_plus2', 'male_minus1', 'male_minus2']
for body in body_morphologies:
    clear_data()
    run(body)
    