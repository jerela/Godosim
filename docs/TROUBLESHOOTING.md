# Troubleshooting and frequently asked questions

## General questions

### I just want to use the annotated images you generated. How do I do that?

You can download the sample dataset on [Zenodo](MISSING).

### How do I generate my own images?

See [here](MISSING).

For advanced users, ...

## Building Godot with OpenSim

## Building and running the binary yourself

### After building Godot with OpenSim integration, building the export template, and exporting the project to create binaries myself, running the binary fails to load background images.

You need to enable the TinyEXR module to be able to load .exr images at runtime. By default, it is enabled for the Godot editor, but not for exported binaries. Navigate to godot/modules/tinyexr/config.py and make can_build() always return True. Then try creating the export template again. See [here](https://github.com/godotengine/godot/issues/71505) for details.