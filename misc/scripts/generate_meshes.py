import os
import torch
from skel.skel_model import SKEL
import trimesh
import sys

from numpy import array2string

if __name__ == '__main__':
    
    args = sys.argv
    print("Arguments: ", args)
    
    
    # read BSM initial pose
    bsm_pose_path = os.path.join('PATH/TO/TEXT/FILE', 'bsm_body_pose.txt')
    f = open(bsm_pose_path, 'r')
    bsm_pose = f.readlines()
    f.close()
    
    
    # initialize settings for SKEL
    device = 'cpu'
    pose = torch.zeros(1, 46).to(device) # (1, 46)
    betas = torch.zeros(1, 10).to(device) # (1, 10)
    trans = torch.zeros(1, 3).to(device)

    for i in range(46):
        pose[0][i] = float(bsm_pose[i])
        print(str(i) + ': ' + str(pose[0][i]))

    # loop through permutations of sex and morphology and generate SKEL output
    for i_gender in ['male', 'female']:
        for i_beta in [-2, -1, 0, 1, 2]:
    
            print("Gender: " + i_gender + ", betas: " + str(i_beta))
    
            # rewrite the body morphology coefficients according to current iteration
            for i in range(len(betas)):
                betas[i] = i_beta
    
            
            # initialize SKEL
            skel = SKEL(gender=i_gender).to(device)

            
            # SKEL forward pass
            skel_output = skel(pose, betas, trans)
            
            if i_beta == -2:
                beta_string = "minus2"
            elif i_beta == -1:
                beta_string = "minus1"
            elif i_beta == 0:
                beta_string = "zero"
            elif i_beta == 1:
                beta_string = "plus1"
            elif i_beta == 2:
                beta_string = "plus2"
            
            filename_identifier = i_gender + "_" + beta_string
            
            # Export meshes    
            os.makedirs('PATH/TO/OUTPUT', exist_ok=True)
            
            filename_skin_mesh = "skin_mesh_" + filename_identifier + ".obj"
            filename_skeleton_mesh = "skeleton_mesh_" + filename_identifier + ".obj"
            
            skin_mesh_path = os.path.join('PATH/TO/OUTPUT', filename_skin_mesh)
            skeleton_mesh_path = os.path.join('PATH/TO/PUTPUT', filename_skeleton_mesh)
            
            trimesh.Trimesh(vertices=skel_output.skin_verts.detach().cpu().numpy()[0], 
                            faces=skel.skin_f.cpu()).export(skin_mesh_path)
            print('Skin mesh saved to: {}'.format(skin_mesh_path))
            
            trimesh.Trimesh(vertices=skel_output.skel_verts.detach().cpu().numpy()[0],
                            faces=skel.skel_f.cpu()).export(skeleton_mesh_path)
            print('Skeleton mesh saved to: {}'.format(skeleton_mesh_path))
            
            
            # write joint translations (positions of joints) to file
            
            joint_translations = (skel_output.joints[0]).tolist()
            #print(joint_translations)
            
            filename_joint_translations = "joint_translations_" + filename_identifier + ".txt"
            joint_path = os.path.join('PATH/TO/OUTPUT', filename_joint_translations)
            
            f = open(joint_path, 'w')
            for joint in joint_translations:
                f.write(str(joint[0]) + "," + str(joint[1]) + "," + str(joint[2]) + "\n")
            f.close()
            #print("Joints:",skel_output.joints)
    
    
            # write bone scales to file
            bone_scales = (skel_output.bone_scales[0]).tolist()
            
            filename_bone_scales = "bone_scales_" + filename_identifier + ".txt"
            bone_scales_path = os.path.join('PATH/TO/OUTPUT', filename_bone_scales)
            
            f = open(bone_scales_path, 'w')
            for scale_factors in bone_scales:
                f.write(str(scale_factors[0]) + "," + str(scale_factors[1]) + "," + str(scale_factors[2]) + "\n")
            f.close()
            
    # note that bones_names and joint_names are the names of bones and joints in SKEL, not necessarily in BSM!
    bone_names = skel_output.bone_names
    joint_names = skel_output.joint_names
    print(bone_names)
    print(joint_names)
    print("SKEL pipeline finished!")
    
    # write bone names to file
    bone_names_path = os.path.join('PATH/TO/OUTPUT', 'bone_names.txt')
    joint_names_path = os.path.join('PATH/TO/OUTPUT', 'joint_names.txt')
    f = open(bone_names_path, 'w')
    for name in bone_names:
        f.write(name + "\n")
    f.close()
    
    # write joint names to file
    f = open(joint_names_path, 'w')
    for name in joint_names:
        f.write(name + "\n")
    f.close()