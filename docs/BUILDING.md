# Advanced building instructions
These instructions are meant for advanced users who wish to fully customize their program. For others, you can use the pre-built binary applications and existing generation protocols. If you insist on building the program yourself, read on.

## Building Godot Engine with OpenSim

## Getting the project files for Godot Editor

## Modifying the OpenSim integration

## 

## SCons workflow

### Building Godot with custom modules

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


