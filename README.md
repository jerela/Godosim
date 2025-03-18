# Godosim
Godot Engine integrating OpenSim musculoskeletal modeling software for generation of synthetic images of human kinematics 

- [Getting started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installing](#installing)
  * [Running the program](#running-the-program)
- [How it works](#how-it-works)
- [Descriptions of files](#descriptions-of-files)
- [Troubleshooting and FAQ](#troubleshooting-and-faq)
  * [General questions](#general-questions)
- [Authors](#authors)
- [License and copyright](#license-and-copyright)
- [Acknowledgements](#acknowledgements)
<!-- toc -->


## Godosim
This repository is the main repository of the Godosim project, which enables the generation of synthetic images of human motion with automatic annotations of anatomical landmarks from OpenSim-compatible musculoskeletal models.

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The prerequisites depend on what you want to use Godosim for. We offer access in three levels of increasing complexity:
1. If you simply wish to access the sample dataset of generated with Godosim, you can find it on [Zenodo](MISSING).
2. If you wish to use the pre-built binary applications and generate your own annotated images while customizing the pipeline from the configuration file, you can download the binaries from the Releases of this repository. The binaries do not include skin meshes, textures, or HDRIs.
   - You can download the HDRIs you wish to use as backgrounds from [Poly Haven](https://polyhaven.com/hdris). In the sample dataset, we used 4K resolution.
   - You can download the prepared SMPL skin meshes from the Releases of this repository. They are [SMPL](https://smpl.is.tue.mpg.de/) meshes generated with [SKEL](https://skel.is.tue.mpg.de/). We are not affiliated with either.
   - You can download skin and clothing textures that are compatible with the prepared skin meshes from the [BEDLAM project page](https://bedlam.is.tue.mpg.de/). Note that to download the textures, you need to agree to BEDLAM's license terms. We are not affiliated with BEDLAM.
     - Instead of SMPL meshes and compatible textures, you can also use your own skin meshes and textures. For instructions on how to do that, see [here](MISSING).
   - See the instructions on [customizing the image generation process from the configuration file](MISSING).
3. **ADVANCED USERS**: If you're a right proper wizard and wish to build your own customized Godosim application, you will need the following in addition to the prerequisites of step 2:
   - [OpenSim 4.5](https://github.com/opensim-org/opensim-core/tree/opensim_451) (included in submodules)
   - [Godot Engine 4.3](https://github.com/godotengine/godot/tree/4.3) (included in submodules)
   - [Custom Godosim C++ module](https://github.com/jerela/godosim-cpp-modules) (included in submodules)
   - [Godosim project files for Godot Engine](https://github.com/jerela/godosim-project-files) (included in submodules)
   - [SCons](https://scons.org/) to build Godot with custom modules. For Godot-specific use instructions, see [the official documentation](https://docs.godotengine.org/en/stable/contributing/development/compiling/introduction_to_the_buildsystem.html).
   - See the instructions on [building Godot Engine and customizing Godosim in Godot Editor](MISSING).


### Installing

Step by step instructions on how to install this project.

#### Windows

#### UNIX

### Running the program

First, make sure you have done one of the following:
- build Godot with OpenSim-integrated custom modules, download the Godot project files, and build the binary **OR**
- simply download the binary for your operating system from [Releases](MISSING)

You are recommended to run the binary through the command line to receive console output that will help you troubleshoot issues that you might encounter. Furthermore, if you wish to access the Godosim demo, you need to run the binary with the command line arguments "--demo".

When you first run the binary, it will generate a config file for you as described [here](/docs/CONFIGURATION.md). Edit the paths in the configuration file to match your file system. You will need to download the following files:
1. skin meshes
	- see [Releases](missinglink
2. textures compatible with the skin meshes
	- you have to register and accept the license agreement to download them from the [BEDLAM project site](https://bedlam.is.tue.mpg.de/)
3. HDRI backgrounds
	- you can download these from [Poly Haven](https://polyhaven.com/hdris)
4. OpenSim-compatible musculoskeletal model
5. OpenSim-compatible kinematics file

## How it works

### SkeletonTracker and custom C++ modules

### Godosim project files

### OpenSim integration

### Using the configuration file

### Output data

## Descriptions of files

### Miscellaneous scripts

## Troubleshooting and FAQ

### General questions

#### I just want to use the annotated images you generated. How do I do that?

You can download the sample dataset on [Zenodo](MISSING).

#### How do I generate my own images?

See [here](MISSING).

For advanced users, ...

### Building Godot with OpenSim

### Building and running the binary yourself

#### After building Godot with OpenSim integration, building the export template, and exporting the project to create binaries myself, running the binary fails to load background images.

You need to enable the TinyEXR module to be able to load .exr images at runtime. By default, it is enabled for the Godot editor, but not for exported binaries. Navigate to godot/modules/tinyexr/config.py and make can_build() always return True. Then try creating the export template again. See [here](https://github.com/godotengine/godot/issues/71505) for details.


## Authors

Jere Lavikainen, jere.lavikainen (at) uef.fi

## License and copyright

### Copyright disclaimer / EULA

TBA

Note that we are not affiliated, endorsed, or sponsored by the creators of OpenSim, Godot Engine, SMPL, BEDLAM, or SKEL. This is an independent project that utilizes their existing work, which is subject to their own individual licenses and terms of use.

## Acknowledgements

TBA

## Publication and citation

TBA
