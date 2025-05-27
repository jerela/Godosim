# Using the configuration file

When running the binary to generate annotated images, many settings are defined in the config file. You can control how the image generation process works by changing the settings.

- [Locating the config file](#locating-the-config-file)
- [Understanding the config file](#understanding-the-config-file)
  * [Descriptions of sections and keys](#descriptions-of-sections-and-keys)
<!-- toc -->


## Locating the config file

When you first run the binary application, it will search for a config file in (USERDATA)*/Godosim/Config/config.cfg*, where (USERDATA) is the path to your persistent user data directory. The exact location depends on your operating system:
- On Windows: *%APPDATA%/Godosim/Config/config.cfg*
- On Linux: *~/.local/share/Godosim/Config/config.cfg*

If the file is not found, one will be created with default settings. Therefore, you should first run the binary application at least once to create the config file. You can also download the config file [here](/misc/other/config.cfg) and place it in the correct location.

## Understanding the config file
The settings in the config file are organized **sections**, **keys**, and **values** in the following format:
```
[section]
key=value
another_key=some_value

[some_other_section]
boolean_setting=true
floating_point=3.14159
message="Hello, world"
```

There must be no whitespaces on either side of the equality *(=)* symbol. Additionally, lines starting with semicolon *(;)* are comments and ignored by the application.
Strings should be enclosed in quotation marks. The data types of values without quotation marks are inferred by the application.
For instance:
```
[generate]
; index where the image generation starts
first_image_index = 0
; how many images will be generated at most (note that this is not the max image iteration, which is first_image_index+max_image_number)
max_image_number=20
; should images be saved
save_images=true
; should csv annotations and labels be saved; note that save_images should be true if this is true
save_csv=true
; "full", "poses", "level", "planar" or something else that's scripted in Generate.gd
iteration_mode="level"
```

If you're not an advanced user, you should only change the values to your liking, but leave sections and keys unchanged.

### Descriptions of sections and keys

In the config file, there are the following sections:
- **paths**: absolute directory paths for the output of the program
- **project_settings**: settings related to the Godot project
- **external_data**: absolute directory paths to where external data (data not included in the binary, such as meshes and 3rd party textures) are
- **skeletontracker**: settings for controlling the OpenSim musculoskeletal simulations
- **bounding_box**: settings for controlling the calculation of the 2D bounding box enclosing the visual avatar in each image
- **generate**: settings for controlling the image generation parameters
- **occlusion-fragmented**: settings for controlling the objects providing visual occlusion in the images, if the *occlusion* key is set to *"fragmented"* under the **generate** section

1. You will need to change the values under **paths** and **external_data** to match your filesystem.
2. You should read through the keys and values in **generate** to understand how you can modify the image conditions.
3. If you wish to change the resolution of the generated images, you can do so under **project_settings**.
4. You probably won't need to look at the other sections.

The names of the keys describe their function, but a commented config file is available [here](/misc/other/config.cfg) for clarity.

#### Explanations of keys by section

##### paths

- **path_output_annotations**
	- absolute directory path to where you want the program to save CSV-formatted annotations and labels for the generated images
- **path_output_images_photos**
	- absolute directory path to where you want the program to save RGB images ("synthetic photos") of the visualized motion
- **path_output_images_silhouette_masks**
	- absolute directory path to where you want the program to save mask images of the silhouette of the visualized human avatar
- **path_output_images_segment_masks**
	- absolute directory path to where you want the progrma to save mask images of individual segments of the visualized human avatar

##### project_settings

- **screen_resolution**
	- the resolution of generated images

##### external_data

- **path_textures_skin_male**
	- absolute directory path to where you keep the texture files for male skin textures
- **path_textures_skin_female**
	- same as above, but for female skin textures
- **path_textures_clothing**
	- absolute directory path to where you keep the texture files for clothing textures (sex-agnostic)
- **path_human_mesh**
	- absolute directory path to where you keep the 3D skin meshes
- **path_hdri**
	- absolute directory path to where you keep the HDRI background images

##### skeletontracker

- **persistent_musculoskeletal_simulation_data**
	- whether you want the program to re-run the simulation whenever we switch between musculoskeletal models (e.g., as a result of changing the sex or weight of the visualized avatar) or keep previously run simulation data and retrieve it instead of re-running
	- true by default, which will retrieve previously simulated data instead of re-running, if such data is available
		- this will improve the performance of the program because a single musculoskeletal model is only simulated once
		- if you have very many different musculoskeletal models in the pipeline, you might want to consider setting this to false, which will make runtime a bit longer but may save memory because the results of all simulations are not stored in memory simultaneously

##### bounding_box
- **vertices**
	- indices of the vertices of the skin mesh
	- if specified, the 3D bounding box will only be generated while considering the vertices at these indices, which may speed up bounding box generation if the number of vertices is limited
	- if specified, **step** will be ignored
	- for example, `vertices=[416, 470, 334, 3347, 504, 4358, 2668, 6464, 2993, 6791, 2938, 6732, 5574, 5682, 5585, 5616, 1764, 1799, 1777, 1807, 5811, 2013, 4558, 707, 3207, 7001, 3881, 3415, 1540, 959, 7160, 5365, 4805, 4947, 1124, 4956, 4964, 1100, 4970, 1110, 1116, 3804, 3686, 7518, 7401, 7469, 7549, 3757, 3836, 3543, 3674, 3699, 7259, 7424, 7411, 7435, 3721]` should provide an accurate bounding box for the SMPL mesh
		- See [here](/misc/other/imported_smpl_vertices.txt) for information about the locations that these indices represent.
	- note that these indices are indices of the mesh once it's imported to Godot Engine, which may affect vertex count, and they do not necessarily match the indices of the SMPL mesh
- **step**
	- how many vertices to skip between each vertex of the skin mesh that is included in finding the bounding box around the skin mesh
	- set to 1 if you want to iterate through all vertices for maximum accuracy but slowest computation speed
	- values above 1 may result in bounding boxes that do not fully enclose all parts of the skin mesh, but will speed up the image generation process significantly
- **padding**
	- how many pixels of padding are added to all four sides of the 2D bounding box after calculating it
	- the use of padding is recommended is **step** is greater than 1

##### generate

- **first_image_index**
	- the image generation process is prepared by constructing a set of parameters (e.g., camera FOV, camera angle, avatar sex and weight, frame of kinematics data for the pose of the avatar, background effects) for different indices
	- this key lets you start from a defined index (e.g., if you want to generate your data in several different runs like generating the first 1000 images in the first run, and another 1000 images in the second run etc)
	- keep at default value 0 unless you know what you're doing
- **max_image_number**
	- defines how many synthetic photos are generated at most
- **save_images**
	- if true, the generated images are saved to file
	- if false, no images are saved
- **save_csv**
	- if true, the annotations and labels are saved to file
	- keep at same value as **save_images**
		- making both false is useful for checking if your custom config values look good without saving anything
- **iteration_mode**
	- you can use this key to switch between image generation presets, e.g., to control if you want images only in a specific motion plane
	- the presets are defined in [Generate.gd](https://github.com/jerela/godosim-project-files/blob/main/Scripts/Generate.gd) in the [project file repository](https://github.com/jerela/godosim-project-files), where you can also add define your own presets
- **occlusion**
	- by default ("none"), there are no external objects occluding the visual avatar in the generated images
	- there are options to add those by setting the value to "fragmented" or "windows" in case you want to augment the images in the 3D scene with occluding objects that interact with the lighting in the scene
- **lighting**
	- daylight lighting ("normal") or very dark lighting ("low")
	- dark lighting can be used to generate low-light images more realistically than modifying the brightness and hues of the images after generation
- **planar_offset**
	- this amount in degrees is added to the rotation of the camera view around the vertical axis
	- e.g., if you want to generate images in the sagittal plane view, you may have to adjust this value to find the sagittal plane
- **bodies**
	- names of bodies in the musculoskeletal model that you want to track (i.e., fetch their 3D transforms and set them to the corresponding bones of the mesh of the visual avatar)
	- this will also define what joints will be tracked, as the joints to track are defined as the joints that are children of tracked bodies
- **path_motion**
	- absolute directory and file path to an existing kinematics file that is used for simulating the motion of the musculoskeletal model and replicating its poses using the visual avatar
- **weights**
	- comma-separated string list of body weight types of the skin mesh, enclosed in square brackets
	- for the default provided SMPL meshes, the names refer to the values of the body shape parameters, which vary between -2 and 2
- **sexes**
	- comma-separated string list of sexes of the skin mesh
- **paths_model**
	- comma-separated list of absolute directory and file paths to the musculoskeletal models (.osim files)
	- assuming "male" is listed before "female" in **sexes**, list musculoskeletal models for male dimensions first and for female dimensions after that
		- similarly, list the musculoskeletal models in the order defined by **weights**
	- see the [example config file](/misc/other/config.cfg)

##### occlusion-fragmented

These keys are read only when **occlusion** under **generate** is set to "fragmented". In that scenario, the visual avatar is surrounded by "pebbles" that visually occlude parts of it. The size and density of pebbles, as well as the radius they are placed on, is controlled by changing the values.

- **pebble_radius_min**
	- minimum radius of a pebble in meters
- **pebble_radius_max**
	- maximum radius of a pebble in meters
- **sphere_radius_min**
	- minimum distance of a pebble from the visual avatar in meters
- **sphere_radius_max**
	- maximum distance of a pebble from the visual avatar in meters
- **pebble_density**
	- controls how many pebbles are created
