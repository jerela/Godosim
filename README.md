# Godosim
Godot Engine integrating OpenSim musculoskeletal modeling software for generating synthetic images of human kinematics 

This is the main repository of the Godosim project, which enables the generation of synthetic images of human motion with automatic annotations of anatomical landmarks from OpenSim-compatible musculoskeletal models.

<details>
<summary>Click to enable GIF of program at work (warning: flashing lights)</summary>
<img src="https://github.com/jerela/Godosim/blob/docs/docs/img/generation_process.gif">
</details>

## Table of contents

- [Getting started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Setting up](#setting-up)
  * [Running the program](#running-the-program)
- [Troubleshooting and FAQ](#troubleshooting-and-faq)
- [Authors](#authors)
- [License and copyright](#license-and-copyright)
- [Acknowledgements](#acknowledgements)
<!-- toc -->

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The prerequisites depend on what you want to use Godosim for. We offer access in three levels of increasing complexity:
1. If you simply wish to access the sample dataset of annotated images generated with Godosim, ~~you can find it on [Zenodo](MISSING)~~ you will have to wait until it's uploaded.
2. If you wish to use the pre-built binary applications and generate your own annotated images while customizing the pipeline from the configuration file, you can follow the instructions on [setting up Godosim](#setting-up).
3. **ADVANCED USERS**: If you're a right proper wizard and wish to build your own customized Godosim application, you will need the following in addition to the prerequisites of step 2:
   - [Godot Engine 4.3](https://github.com/godotengine/godot/tree/4.3) (included in submodules)
   - [Custom Godosim C++ module](https://github.com/jerela/godosim-cpp-modules) (included in submodules)
   - [Godosim project files for Godot Engine](https://github.com/jerela/godosim-project-files) (included in submodules)
   - [SCons](https://scons.org/) to build Godot with custom modules. For Godot-specific use instructions, see [the official documentation](https://docs.godotengine.org/en/stable/contributing/development/compiling/introduction_to_the_buildsystem.html).
   - See the instructions on [building Godot Engine](/docs/BUILDING.md) and [customizing Godosim](/docs/CUSTOMIZING.md) or check the [GitHub Actions workflow file](missing) in this repository.


### Setting up

Step by step instructions on how to install and set up this project and its dependencies.

1. Install [OpenSim 4.5](https://simtk.org/frs/?group_id=91)
	- You will need to register to SimTK for free to be able to download OpenSim.
1. Download the Godosim binary executable from [Releases](https://github.com/jerela/Godosim/releases/tag/v1.0.0)
3. The executable uses the shared libraries of OpenSim. You need to tell the operating system where to find them.
	- Find the **bin** directory in your OpenSim installation root directory, and add it to the PATH environmental variable.
4. Next, you need to download assets that Godosim uses.
	1. Download skin meshes from [Releases](https://github.com/jerela/Godosim/releases/tag/v1.0.0).
		- These are [SMPL](https://smpl.is.tue.mpg.de/) meshes generated with [SKEL](https://skel.is.tue.mpg.de/).
	2. Download scaled MSK models corresponding to the skin meshes from [Releases](https://github.com/jerela/Godosim/releases/tag/v1.0.0).
	3. Download a pre-calculated motion file that is compatible with the scaled MSK models from [SimTK](https://simtk.org/frs/?group_id=516).
		- You need to download the first package, **Simulation of Human Running**. From the archive, you need to find the file **RunningSimulation_simTK/IK/subject02_running.trc** and extract it.
 	4. Download skin and clothing textures for the skin meshes from the [BEDLAM project page](https://bedlam.is.tue.mpg.de/).
		- You will need to register for free and accept the license terms to be able to download the files.
		- The files you need are **body textures** (1.8 GB) and **clothing overlay textures** (5.3 GB). You do not need the other BEDLAM files.
		- Extract and move the ones you want to use to folders.
			- Body textures for males and females should have their own folders.
			- The clothing textures should have their own folder without separation by sex.
	5. Download some HDRI backgrounds from [Poly Haven](https://polyhaven.com/hdris).
 		- In the sample dataset, we used 4K resolution.
		- Make a folder to put them in.
5. Now you need to configure your **config.cfg** file. When you run Godosim for the first time, it creates one for you. Alternatively, you can download it [here](/misc/other/config.cfg).
	- You need to define where you keep the skin meshes, scaled MSK models, motion file, clothing and skin textures, and HDRI backgrounds.
 		- See [here](/docs/CONFIGURATION.md#descriptions-of-sections-and-keys) for instructions on filling the path values.
   	- More information below in [Running the program](#running-the-program)
6. You can now run the program from the binary executable. See [Running the program](#running-the-program) below.

### Running the program

Make sure you have first followed the instructions in [Setting up](#setting-up)
You are recommended to run the binary from the command line to receive console output that will help you troubleshoot issues that you might encounter. Furthermore, you can run the binary with the command line argument "--demo" to access a demonstration scene that lets you manually experiment with how the program works.

When you first run the program, it will generate a config file for you as described [here](/docs/CONFIGURATION.md). Edit the paths in the configuration file to match your file system. Once the correct paths are in and you run the program, you will see a screen where a visual avatar of a human is shown in various poses, clothing and skin textures, and with various backgrounds. The GIF animation at the top of this readme demonstrates the procedure.

Once the generation procedure is finished, the program will write the output to the directories specified in the config file and then close.

## Troubleshooting and FAQ

See [here](/docs/TROUBLESHOOTING.md).


## Authors

Jere Lavikainen, jere.lavikainen (at) uef.fi

## License and copyright

The [scripts](/misc/scripts) are licensed under the [MIT license](/misc/scripts/LICENSE).

**The MIT license does not apply to the generated image dataset**, which is only available for noncommercial use. Additionally, **the MIT license does not apply to the non-code files included in the Releases**; the Releases contains some files (e.g., 3D meshes) that have a separate license.

We are not affiliated, endorsed, or sponsored by the creators of OpenSim, Godot Engine, SMPL, BEDLAM, or SKEL. This is an independent project that utilizes their existing work, which is subject to their own individual licenses and terms of use.

## Acknowledgements

A big thanks to the helpful Godot Engine community, particularly [R Hill](https://github.com/partybusiness), who helped greatly with the [body mask shader](https://github.com/jerela/godosim-project-files/blob/master/Shaders/body_mask.gdshader).

## Publication and citation

TBA
