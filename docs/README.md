# Spans

Small, unfinished 3D renderer for the Game Boy Advance.

- All code written in ARM assembly
- Export models from Blender
- Fast solid-filled triangles
- Subpixel accuracy
- Currently renders [Suzanne](https://en.wikipedia.org/wiki/Blender_(software)#Suzanne,_the_%22monkey%22_mascot) (968 triangles) at ~40 FPS.

![Demo](https://user-images.githubusercontent.com/8228102/206881963-b94d7fb2-cb74-46b0-8c2a-9f7ef2abff3f.gif)

[Download demo ROM](https://github.com/vanjac/spans/releases/latest/download/spans.gba)

You will need devkitPro to build. The Makefile uses my ["inline alias"](https://github.com/vanjac/gas-inline-alias) preprocessor script for assembly files, which requires Python 3.
