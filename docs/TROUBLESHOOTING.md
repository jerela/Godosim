# Troubleshooting and frequently asked questions

## General questions

### I just want to use the annotated images you generated. How do I do that?

You can download the sample dataset on [Zenodo](MISSING).

### How do I generate my own images?

See [here](MISSING).

For advanced users, ...

## Running the pre-built binary executable

### When I run the program, nothing happens or a black window appears for an extended period of time.

Run the program from your command line to get more specific information.

### When I run the program, I get errors about missing paths.

Make sure the paths in [your configuration file](/docs/CONFIGURATION.md) are correct. Additionally, make sure you use forward slashes */* instead of backslashes *\\* as directory separators.

### When I run the program, the screen remains black. If any images are generated, they are black or mostly black with some noise. Multiple error messages appear in the console, including something about *VK_SUCCESS*.

This is because your device does not support the Vulkan renderer of Godot. Try updating your GPU driver and trying again. If it doesn't help, you can run Godot with a compatibility renderer. To do so, run the program with the argument *--rendering-method gl_compatibility*. For example:
`godosim-windows-x86-64.exe --rendering-method gl_compatibility`

## Building Godot with OpenSim

## Building and running the binary yourself

### After building Godot with OpenSim integration, building the export template, and exporting the project to create binaries myself, running the binary fails to load background images.

You need to enable the TinyEXR module to be able to load .exr images at runtime. By default, it is enabled for the Godot editor, but not for exported binaries. Navigate to godot/modules/tinyexr/config.py and make can_build() always return True. Then try creating the export template again. See [here](https://github.com/godotengine/godot/issues/71505) for details.