This is a codebase intended to be used with userland title exploits in general for Nintendo 3DS. This repo generates a ropkit.bin rop code file that loads a *hax payload, executes it, which in turn loads the homebrew menu.

Prep: Find an exploit in a 3DS userland appliction and get rop execution (surprise!). The scripts in this repo require [ropgadget_patternfinder](https://github.com/yellows8/ropgadget_patternfinder). Place this compiled .exe in your PATH somewhere or in this directory. Install python3 if you wish to run the .py version of generate_ropinclude (this is recommended for windows users). Install the 3DS toolchain from devkitpro.org on your computer if you haven't already.

1) Dump the NCCH of your target userland application and extract the code.bin by running [ctrtool](https://github.com/3dshax/ctr/tree/master/ctrtool) --exefsdir=exefs game.cxi. Alternatively, you can use [GodMode9](https://github.com/d0k3/GodMode9) by navigating to: SYSNAND SD:/title/<target titleID>/content/00000000.tmd -> TMD file options -> Extract .code, to get your decompressed codebin. Rename to code.bin and place it in this directory.

2) Run "generate_ropinclude code.bin data" from the command line in this directory. A list of defines should appear on your terminal. Copy these inside the includes.h file and save. Note that some of these gadget defines may be missing (you will notice the "//WARNINGS"). With a few, that is okay, but most will need to be found if ropkit is to work. Experimention and debugging might be necessary to find work-arounds.

3) Double check that the #defines in the ropkit.s file fit the context of your userland app. When satisfied, run Make in this repo to generate ropkit.bin.

4) Find a way to load ropkit.bin into memory (virt. address "ROPBUFF" in ropkit.s), and then stack pivot to it from your exploit rop. Ropkit should handle the rest.


# ropkit_boototherapp.s
This handles booting the otherapp \*hax payload, various defines are required.

This automatically handles locating each 0x1000-byte page in .text used with the payload in physmem, across the entire APPLICATION memregion. Hence, this bypasses the codebin physmem randomization added with v10.4, which was later enabled for more titles with v11.0.

