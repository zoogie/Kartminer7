#define ROP_POPPC 0x001017b8
#define POP_R1PC 0x00109d6c
#define POP_R3PC 0x00102d70
#define POP_R0R2PC 0x15dbc8+1 //: pop {r0, r1, r2, pc}
#define POP_R2R6PC 0x00107b50
#define POP_R4LR_BXR1 0x00103704
#define POP_R4R8LR_BXR2 0x0013687c
#define POP_R4R5R6PC 0x0010013c
#define POP_R4FPPC 0x00100938
#define POP_R4R8PC 0x0010103c

#define ROP_STR_R1TOR0 0x001066f4
#define ROP_STR_R0TOR1 0x00100684
#define ROP_LDR_R0FROMR0 0x00111d38
#define ROP_ADDR0_TO_R1 0x00111d60

#define MEMCPY 0x0010f548

#define svcSleepThread 0x00105c58

#define GSPGPU_FlushDataCache 0x00113430
#define GSPGPU_SERVHANDLEADR 0x0066890c

#define IFile_Read 0x001016d4
#define IFile_Write 0x00102fac

#define ROP_POPR3_ADDSPR3_POPPC 0x001144e4
#define POP_R0PC 0x0011a698
#define ROP_LDRR1R1_STRR1R0 0x0044095c
#define POP_R5R6PC 0x00121154
#define ROP_CMPR0R1_ALT0 0x00380ca0
#define MEMSET32_OTHER 0x0010c248
#define svcControlMemory 0x00101538
#define ROP_INITOBJARRAY 0x0010d5c8
#define svcCreateThread 0x00102cdc
#define svcConnectToPort 0x00105c1c
#define svcGetProcessId 0x00105c34
//WARNING: THROWFATALERR_IPC not found.
#define SRV_GETSERVICEHANDLE 0x00106444
#define CFGIPC_SecureInfoGetRegion 0x00190238
#define ROP_COND_THROWFATALERR 0x00105de4
#define GXLOW_CMD4 0x00113534
#define GSP_SHAREDMEM_SETUPFRAMEBUF 0x00230a94
#define GSPTHREAD_OBJECTADDR 0x0065ac40
//WARNING: FS_MountSdmc not found.
#define  IFile_Open 0x00102d7c
#define IFile_Close 0x102ea0
#define IFile_Seek 0x001891a4
