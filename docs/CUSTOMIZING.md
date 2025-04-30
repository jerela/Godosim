# Customizing the Godosim workflow

## Using your own musculoskeletal models, skin meshes, or textures

The preparation of skin meshes involves matching their deformation to the 3D transforms of bones of a musculoskeletal model.

The default skin meshes use SMPL meshes generated with SKEL. Because the musculoskeletal model of SKEL is not fully compatible with OpenSim, the skin meshes distributed with Godosim use the Hamner musculoskeletal model. In a nutshell, the skeletal structure of the Hamner model is scaled and fitted to the joint positions of the SKEL model. The process involves several steps:
1. Generating SMPL meshes with SKEL in a static standing pose
	- See [here](/misc/scripts/generate_meshes.py) and [here](/docs/misc/other/bsm_body_pose.txt) for examples.
2. Extracting the joint translations of the SKEL musculoskeletal model from the generated SMPL meshes
	- See [here](/misc/scripts/generate_meshes.py)
3. Scaling the body dimensions of the Hamner model using the joint translations of the SKEL model
	- See [here](/misc/scripts/fit_osim_to_skel.m)
4. Fitting the pose of the scaled Hamner model to the joint translations of the SKEL model
	- See [here](/misc/scripts/fit_osim_to_skel.m)
5. Importing the SMPL mesh from step **1** in Blender and rigging it by generating an armature with bones that recreate the scaled and posed Hamner model
	- See [here](/misc/scripts/Blender_skin_and_rig.py)
6. Skinning the SMPL mesh to enable its deformation with the bones
	- See [here](/misc/scripts/Blender_skin_and_rig.py)
7. Enabling the UV map of SMPL on the SKEL-outputted skin mesh so that SMPL textures can be used with the skin mesh
	- See [here](/misc/scripts/Blender_skin_and_rig.py)

After this, the rigged and skinned SMPL mesh can be used in a game engine, and if its bones are set to 3D transforms read from an OpenSim simulation, the mesh will deform accordingly.

You can follow a similar workflow to use other musculoskeletal models, meshes, or textures.

## Customizing the image generation protocol in Godot Editor

You can use the Godot editor to open the [Godosim project files](https://github.com/jerela/godosim-project-files) and modify how the program works.
	- The script [Generate.gd](https://github.com/jerela/godosim-project-files/blob/master/Scripts/Generate.gd) contains the image generation process.
		- The function *prepare_parameters()* calculates the different values for avatar weight and sex, background image, frame of motion data, skin and clothing textures, and camera parameters to be used during image generation.
			- Different image generation protocols, which are controlled with **iteration_mode** in [config.cfg](/misc/other/config.cfg), are defined in this function. You can also write your own.
	- The script [HumanModel.gd](https://github.com/jerela/godosim-project-files/blob/master/Scripts/HumanModel.gd) contains the bindings to the OpenSim-to-Godot integration and defines how the pose of the visual avatar is controlled.
		- See the functions *run_simulation()* and *visualize_frame()* in particular.

## Modifying the OpenSim integration

See the [SkeletonTracker](https://github.com/jerela/godosim-cpp-modules/blob/main/godosim/SkeletonTracker.h) class for direct access to the C++ module that utilizes OpenSim.