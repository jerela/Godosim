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

If the file is not found, one will be created with default settings. Therefore, you should first run the binary application at least once to create the config file. You can also download the config file [here](/misc/config.cfg) and place it in the correct location.

## Understanding the config file
The settings in the config file are organized **sections**, **keys**, and **values** in the following format:
```
[section]
key=value
anotherKey=someValue

[someOtherSection]
booleanSetting=true
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
- **generate**: settings for controlling the image generation parameters
- **occlusion-fragmented**: settings for controlling the objects providing visual occlusion in the images, if the *occlusion* key is set to *"fragmented"* under the **generate** section

1. You will need to change the values under **paths** and **external_data** to match your filesystem.
2. You should read through the keys and values in **generate** to understand how you can modify the image conditions.
3. If you wish to change the resolution of the generated images, you can do so under **project_settings**.
4. You probably won't need to look at the other sections.

The names of the keys describe their function, but a commented config file is available [here](/misc/config.cfg) for clarity.
