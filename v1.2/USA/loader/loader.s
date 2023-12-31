	.arm
	.text
	
#include "includes.h"    				//created by running the generate_ropinclude(.sh/.py) script on your target app's code.bin

/* note that these below defines will likely be different app to app */
#define GARBAGE 0x44444444
#define NOP 0xe1a00000
#define STACK_PIVOT ROP_POPR3_ADDSPR3_POPPC
#define STACK_PIVOT2 0x12f6c0

#define ROPBUF 0x14220000  				//virtual memory location of rop payload (ropkit.bin) that launches otherapp. make sure the address in the makefile matches this define
//#define ROPKIT_BINPAYLOAD_ADDR 0x1579d860 + 0x1000
#define ROPKIT_LINEARMEM_REGIONBASE 0x14000000   	//would be 0x30000000 for newer titles (roughly firmware 8.0 and above)
#define ROPKIT_LINEARMEM_BUF (ROPKIT_LINEARMEM_REGIONBASE+0x200000)

//#define ROPKIT_MOUNTSD					//not all titles can access the sdmc! some will need to read otherapp from the savefile
//#define ROPKIT_MOUNTSAVEDATA
//#define ROPKIT_BINPAYLOAD_PATH "sd:/otherapp.bin"       //would be "data:/otherapp.bin" for a savedata mount
//#define ROPKIT_TMPDATA ROPKIT_LINEARMEM_BUF-0x10000         		//this is the default address
#define ROPKIT_BINLOAD_TEXTOFFSET 0x4d0000		//this is virtual address 0x00101000, the default entrypoint of *hax otherapp payloads
//#define ROPKIT_BINPAYLOAD_FILEOFFSET
#define ROPKIT_ENABLETERMINATE_GSPTHREAD
#define ROPKIT_BEFOREJUMP_CACHEBUFADDR (ROPKIT_LINEARMEM_REGIONBASE+0x200000)
#define ROPKIT_BEFOREJUMP_CACHEBUFSIZE 0x800000  	//large gsgpu flush fixes our new3ds L2 cache issues - and increases stability for old3ds
#define UBL_ 0x64f665+1             //skip the first letter since its mounted already by app (sd:/)
#define UBL_UBLL_LST 0x652bc4+2    //reload unabridged sd:/data.dat with remaining payload files embedded. no more heap guesswork.
#define FS_MountExtSavedata 0x186EBC
#define GSP_WRITEHWREGS 0x111fc0
#define HWREGS_ADDR 0x0202A04
#define STR_R0R1_POPR4PC 0x106010


#include "ropkit_ropinclude.s"
.global _start
_start:
ropstackstart:

#include "ropkit_boototherapp.s"  

ropkit_cmpobject:
.word (ROPBUFLOC(ropkit_cmpobject) + 0x4) @ Vtable-ptr
.fill (0x40 / 4), 4, STACK_PIVOT @ Vtable