3D renderer for the GBA. Work in progress.

- Export models from Blender
- Fast solid-filled triangles
- Subpixel accuracy
- Currently renders [Suzanne](https://en.wikipedia.org/wiki/Blender_(software)#Suzanne,_the_%22monkey%22_mascot) (968 triangles) at ~40 FPS.

You will need devkitPro to build. The Makefile uses my ["inline alias"](https://github.com/vanjac/gas-inline-alias) preprocessor script for assembly files, which requires Python 3.