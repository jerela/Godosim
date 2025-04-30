# Advanced building instructions
These instructions are meant for advanced users who wish to fully customize their program. For others, you can use the pre-built binary applications and existing generation protocols. If you insist on building the program yourself, read on.

## Building Godot Engine with OpenSim

Follow the [Godot documentation on building Godot with custom modules](https://docs.godotengine.org/en/stable/contributing/development/core_and_modules/custom_modules_in_cpp.html).
You can get the Godosim C++ module(s) [here](https://github.com/jerela/godosim-cpp-modules).

## Getting the project files for Godot Editor

You can download the [project files](https://github.com/jerela/godosim-project-files) and open them in Godot Editor like any other Godot project. Note that you will need to use a custom build of Godot as described in the previous step.

## Modifying the OpenSim integration

The [SkeletonTracker C++ class](https://github.com/jerela/godosim-cpp-modules/blob/main/godosim/SkeletonTracker.h) defines the OpenSim functionalities. See [Building Godot Emgome with OpenSim](#building-godot-engine-with-opensim) for instructions on how to use it with Godot.

## SCons workflow

Godot uses SCons for building. For details, see the Godot documentation [here](https://docs.godotengine.org/en/stable/contributing/development/compiling/introduction_to_the_buildsystem.html).

### Building export templates

Before exporting the project files into a binary, you need to create a custom export template that includes the Godosim C++ modules. Exactly what you require depends on your operating system.

The instructions in the Godot documentation are for creating export templates without custom modules. To include custom modules, you need to specify their path in the command. You also need to specify the directory where you installed OpenSim. Examples are provided below in platform-specific instructions.

#### Windows

See **Creating Windows export templates** [here](https://docs.godotengine.org/en/stable/contributing/development/compiling/compiling_for_windows.html).
For example:
```
scons platform=windows target=template_release arch=x86_64 vsproj=no custom_modules=../godosim-cpp-modules opensim_install_dir="C:/OpenSim 4.5b"
```

#### Linux

See **Building export templates** [here](https://docs.godotengine.org/en/stable/contributing/development/compiling/compiling_for_linuxbsd.html).
For example:
```
scons platform=linuxbsd target=template_release arch=x86_64 vsproj=no custom_modules=../godosim-cpp-modules opensim_install_dir="C:/OpenSim 4.5b"
```

### Exporting to binary files

See the relevant Godot documentation [here](https://docs.godotengine.org/en/latest/tutorials/export/exporting_projects.html).
Additionally, the GitHub Actions workflow file of this repository demonstrates how to export via command line.