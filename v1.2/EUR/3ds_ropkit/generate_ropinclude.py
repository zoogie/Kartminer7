import os,sys,subprocess

ROPKIT_PATTERNFINDER_BLACKLISTPARAM=""
r=0	#cmd function result

SC=len(sys.argv)
S1=sys.argv[1] #code.bin
S2=sys.argv[2] #script directory

if SC > 3:
	if sys.argv[3].lower() == "--disableblacklist":
		ROPKIT_PATTERNFINDER_BLACKLISTPARAM=""
		print("//Blacklist disabled")

def cmd(s):  # process the ropgadget_patternfinder call string
	global r
	out=""
	try:
		out=subprocess.check_output(s)
		print(out.decode("utf-8"),end="")
		r=0
	except:
		r=-1

# *************************************************************************************************************************************************************************
# Run gadget list script
printstr='ropgadget_patternfinder %s --script=%s/ropkit_ropgadget_script --baseaddr=0x100000 %s --patterntype=sha256' % (S1,S2,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
r=subprocess.call(printstr)
if r:
	print("//WARNING: %s/ropkit_ropgadget_script exited due to a missed gadget.\n" % S2)


# *************************************************************************************************************************************************************************
# Locate ROP_POPR3_ADDSPR3_POPPC(not always available).
# This pops r3 from stack, adds sp with r3, then pops pc from stack.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=47a687d3e467da0eb5fdd711ed9c94b043152bab2fbbbecc29ec2d6308da0494 --patternsha256size=0xc "--plainout=#define ROP_POPR3_ADDSPR3_POPPC "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	print("//WARNING: ROP_POPR3_ADDSPR3_POPPC not found.")


# *************************************************************************************************************************************************************************
# Locate the gadget for setting r0.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=e0160ca8a7f0ec85bd4b01d8756fb82e38344124545f0a7d58ae2ac288da17cc --patternsha256size=0x4 "--plainout=#define POP_R0PC "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	# This one does: r0 = *(sp+0), then pops r3 and pc from stack.
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=4ab819e1f53dd13355b6fc83fff9ff36e82e3866bb6da0f546221a457ba1a54d --patternsha256size=0x8 "--plainout=#define ROP_LDRR0SP_POPR3PC "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		print("//WARNING: POP_R0PC/ROP_LDRR0SP_POPR3PC not found.")
	

# *************************************************************************************************************************************************************************
# Locate ROP_LDRR1R1_STRR1R0 here since it's not always available.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=aa6a623d7c3291340160fd74738249e68b3b4ac2b59cd2c9b5846adcfefb702f --patternsha256size=0xc "--plainout=#define ROP_LDRR1R1_STRR1R0 "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	print("//WARNING: ROP_LDRR1R1_STRR1R0 not found.")


# *************************************************************************************************************************************************************************
# Locate POP_R5R6PC here since it's not always available.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=6ba53f3ece56d84fae11a675a32bf9a6cb4f2036f01a6da0932ade8a5878e001 --patternsha256size=0x4 "--plainout=#define POP_R5R6PC "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	print("//WARNING: POP_R5R6PC not found.")


# *************************************************************************************************************************************************************************
# Locate the gadget for ROP_CMPR0R1.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=947b973f3ad1e3073fa0aaf9e05314cb7f95cb0bbdde1d0f2b65e75c854be08e --patterndatamask=ffffffff00ffffff00ffffffffffffff --patternsha256size=0x10 "--plainout=#define ROP_CMPR0R1 "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	# This one executes "cmp r0, r1", updates r0 depending on the result, then executes bx-lr.
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=97b394def410a11df8cc645a58ed647c43aeb17fd0491b3ba336f059be39e74f --patternsha256size=0x14 "--plainout=#define ROP_CMPR0R1_ALT0 "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		# The same name is used here since this would be used the same way in the ROP-chain, even though the functionality is different.
		printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=6fada5834ebff9c9baf94ad60e873cf97613a5b2f8748ed39f0faa14758396be --patternsha256size=0x18 "--plainout=#define ROP_CMPR0R1_ALT0 "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
		cmd(printstr)
		if r:
			# The comment for the above pattern applies for this one too.
			printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=1fe92f9bb37de52b947db019749a9e7693b246f71a0be7de624d633f80c95184 --patternsha256size=0x18 "--plainout=#define ROP_CMPR0R1_ALT0 "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
			cmd(printstr)
			if r:
				print("//WARNING: ROP_CMPR0R1* not found.")
			

# *************************************************************************************************************************************************************************
# Locate MEMSET32_OTHER.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=730f1de429d80d0f5e921d483b8078909870c94538bd3b400f1823010ab4c53e --patternsha256size=0x28 "--plainout=#define MEMSET32_OTHER "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=e1a8a23776be0edde9d846f79f3a63c8652b629ae7a105aef8eb3e70c490ba7f --patternsha256size=0x28 "--plainout=#define MEMSET32_OTHER "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		print("//WARNING: MEMSET32_OTHER not found.")
	

# *************************************************************************************************************************************************************************
# Locate svcControlMemory.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=830c604f4c125a2e0bf80a8716809e21a75b0cd93e7a2c3a4bf4b096117f195c --patternsha256size=0x10 "--plainout=#define svcControlMemory "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	print("//WARNING: svcControlMemory not found.")


# *************************************************************************************************************************************************************************
# Locate ROP_INITOBJARRAY.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=ea2d9f91d1fdb4bc29803e1f24dafd5b2f3aa3455579e356448933f149132243 --patternsha256size=0x18 "--plainout=#define ROP_INITOBJARRAY " --addval=0x1' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	# Older version of the above, in ARM-mode.
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=e3691cfe859e38d854b7e31a7413a8a6098f4f9ddcff61db996fb8e538fef169 --patternsha256size=0x40 "--plainout=#define ROP_INITOBJARRAY "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		# Another version of the above.
		printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=290002253638463182bd3ec5fe8636aa6c7726aa0eacf9009e2a14bf7ba6639e --patternsha256size=0x40 "--plainout=#define ROP_INITOBJARRAY "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
		cmd(printstr)
		if r:
			print("//WARNING: ROP_INITOBJARRAY not found.")
		

# *************************************************************************************************************************************************************************
# Locate svcCreateThread.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 --patterntype=sha256 --patterndata=0103df5f7916ca91a0c1698573ae7878a488c5df5f01e717f336dca82262b6a9 --patternsha256size=0x24 "--plainout=#define svcCreateThread "' % (S1)
cmd(printstr)
if r:
	print("//WARNING: svcCreateThread not found.")


# *************************************************************************************************************************************************************************
# Locate svcConnectToPort.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=64a052c8f577f2b6810b6bc488bb14e745f1066195dc14f498aea8e82245b0c4 --patternsha256size=0x18 "--plainout=#define svcConnectToPort "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	print("//WARNING: svcConnectToPort not found.")


# *************************************************************************************************************************************************************************
# Locate svcGetProcessId.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=429c407642c36bdf169d167bf3efc7a0eb4cf5052a08a97fc56ecbcfdb96f1b8 --patternsha256size=0x18 "--plainout=#define svcGetProcessId "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	print("//WARNING: svcGetProcessId not found.")


# *************************************************************************************************************************************************************************
# Locate the ipc command function for throwfatalerror.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=184f0cd7d0fe37a8990cf02e8500bb4267a7e23ae14c8d2b76a5f6ae756c7345 --patterndatamask=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffffffffffff --patternsha256size=0x38 "--plainout=#define THROWFATALERR_IPC "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	print("//WARNING: THROWFATALERR_IPC not found.")


# *************************************************************************************************************************************************************************
# Locate SRV_GETSERVICEHANDLE.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=883dc75d232f768ecafc1d6fd569c3b8301b1eda5ef5d52392872eed9be7f015 --patterndatamask=ffffffff00ffffffffffffffffffffffffffffffffffffffff --patternsha256size=0x18 "--plainout=#define SRV_GETSERVICEHANDLE "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	# Older version of the above.
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=8c3af44c29096e3e1d07f7435027cc22fda8437264e9542ac47280b1a01c1010 --patternsha256size=0x20 "--plainout=#define SRV_GETSERVICEHANDLE "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		print("//WARNING: SRV_GETSERVICEHANDLE not found.")
	

# *************************************************************************************************************************************************************************
# Locate CFGIPC_SecureInfoGetRegion.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=18f4341ba0caf2c160825b63587aeff7d4e0edec4d4107fecc06127b4cb9726b --patternsha256size=0x2c "--plainout=#define CFGIPC_SecureInfoGetRegion "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	# Older version of the above.
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=6132230265fd553f4ba25fbbb857f0119204c147a7f88d5d08f7e4a1bf60d335 --patternsha256size=0x3c "--plainout=#define CFGIPC_SecureInfoGetRegion "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		print("//WARNING: CFGIPC_SecureInfoGetRegion not found.")
	

# *************************************************************************************************************************************************************************
# Locate the gadget for the conditional throw_fatalerror().
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 --patterntype=sha256 --patterndata=871fa0535022597b28d37811aa235ea59f56dd7b02d813c7a3dbc38306efc82b --patterndatamask=ffffffffffffffffffffffffffffffff000000ffffffffff --patternsha256size=0x18 "--plainout=#define ROP_COND_THROWFATALERR "' % (S1)
cmd(printstr)
if r:
	# This one does: r1 = r0_bit31, call throw_fatalerror() when r1 is non-zero. r0 = u32 @ sp+0. Then r3 and pc are popped from stack.
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 --patterntype=sha256 --patterndata=53f02c08f14ce994623440dfa3107c98ce750470d1c68567a353e834cd3aa234 --patterndatamask=ffffffff000000ffffffffffffffffff --patternsha256size=0x10 "--plainout=#define ROP_COND_THROWFATALERR_ALT0 "' % (S1)
	cmd(printstr)
	if r:
		print("//WARNING: ROP_COND_THROWFATALERR* not found.")
	

# *************************************************************************************************************************************************************************
# Locate GXLOW_CMD4.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=406e130dfe0a99ba64c16ac6ec4a53355cb36f090647b73c5382ea180c88e72c --patternsha256size=0x30 "--plainout=#define GXLOW_CMD4 "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=92aaae0b22699ada29758d0f9c7043897b634196c87c0e6a3c9f562e221d751d --patternsha256size=0x3c "--plainout=#define GXLOW_CMD4 "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		print("//WARNING: GXLOW_CMD4 not found.")
	

# *************************************************************************************************************************************************************************
# Locate GSP_SHAREDMEM_SETUPFRAMEBUF.
# Newest version.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=39b7de81819a6efcff6a796bf180f0b76672485a7aebe40113580d73df1d2f44 --patterndatamask=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --patternsha256size=0x94 "--plainout=#define GSP_SHAREDMEM_SETUPFRAMEBUF "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	# From system-version v3.0.
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=a78a6ea171b8ecbcf648eb77ee932b14851a1f302b02e7aaa8a4a5e4d8df0ca6 --patterndatamask=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --patternsha256size=0x98 "--plainout=#define GSP_SHAREDMEM_SETUPFRAMEBUF "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		# From system-version v1.0.
		printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=03264e88cf05c243ecd176841c11769b60b14f1bac95f7422abe82ab2d322fd2 --patterndatamask=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --patternsha256size=0xc4 "--plainout=#define GSP_SHAREDMEM_SETUPFRAMEBUF "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
		cmd(printstr)
		if r:
			print("//WARNING: GSP_SHAREDMEM_SETUPFRAMEBUF not found.")
		

# *************************************************************************************************************************************************************************
# Locate GSPTHREAD_OBJECTADDR.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 --patterntype=sha256 --patterndata=ac35305d80ce0c7e3a312a2704c08e67d54c2b6020c918c06b2d6c86fef74334 --patternsha256size=0x5c --dataload=0x80 "--plainout=#define GSPTHREAD_OBJECTADDR "' % (S1)
cmd(printstr)
if r:
	print("//WARNING: GSPTHREAD_OBJECTADDR not found.")


# *************************************************************************************************************************************************************************
# Locate FS_MountSdmc.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=e25b7bfb96863f69fcbef8fdad176da9dff3e72502c1f2ca837115b3fc290212 --patternsha256size=0x10 "--plainout=#define FS_MountSdmc "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	print("//WARNING: FS_MountSdmc not found.")


# *************************************************************************************************************************************************************************
# Locate FS_MountSavedata.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=ff6e2e8495967faa7c7a25c6f5ab5a6ab571b3557bd1cf2fed6bcf344a3da892 --patterndatamask=ffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --patternsha256size=0x4c "--plainout=#define FS_MountSavedata "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	# Newer version of the above.
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=92ba31c704c29ef4549b18dad28138b449f3e55f035640bd306dc01e7cac0ad2 --patterndatamask=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --patternsha256size=0x6c "--plainout=#define FS_MountSavedata "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		# Newer version of the above.
		printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=e7d553ccf1cac7d3efe4d7fc441564368f346271d320746b507331545075776c --patterndatamask=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --patternsha256size=0x74 "--plainout=#define FS_MountSavedata "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
		cmd(printstr)
		if r:
			print("//WARNING: FS_MountSavedata not found.")
	

# *************************************************************************************************************************************************************************
# Locate IFile_Open.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=f12b196453c8d76905a0abe3a5395295471ba44f4b1ac6d3fe7f585b59c217ec --patternsha256size=0x18 "--plainout=#define IFile_Open "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=5e4960e460a86bd40ddf00ea5981da01c4ec6246a40d28138976629c4e298fe5 --patternsha256size=0x18 "--plainout=#define IFile_Open "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
	cmd(printstr)
	if r:
		print("//WARNING: IFile_Open not found.")
	

# *************************************************************************************************************************************************************************
# Locate IFile_Close.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 %s --patterntype=sha256 --patterndata=d2dfec7874a22d753a2715e6ad640e0572d6b3d86d12792762d259ff0216705e --patternsha256size=0x18 "--plainout=#define IFile_Close "' % (S1,ROPKIT_PATTERNFINDER_BLACKLISTPARAM)
cmd(printstr)
if r:
	#If locating the function via the actual function code fails(newer version of that code), try locating it via code calling it instead.
	fail=0
	
	cmdstr="ropgadget_patternfinder %s --baseaddr=0x100000 --patterntype=sha256 --patterndata=ca3add997a4d158ec6815506271f20d23d2c1d3a0c33dc85f8ed65e3cfc8d260  --patterndatamask=00fff0ffffffffff000000ff --patternsha256size=0xc --plainout=" % S1
	
	printstr='%s --addval=0x8' % cmdstr
	try:
		r=subprocess.check_output(printstr)
		rawaddr=int(r,16)
	except:
		fail=1
	
	printstr='%s --dataload=0x8' % cmdstr
	try:
		r=subprocess.check_output(printstr)
		tmpdata=int(r,16)
	except:
		fail=1

	if not fail:
		print("#define IFile_Close 0x%x" % (rawaddr+0x8 + ((tmpdata & 0xffffff)<<2)))
	else:
		print("//WARNING: IFile_Close not found.")
	

# *************************************************************************************************************************************************************************
# Locate IFile_Seek.
printstr='ropgadget_patternfinder %s --baseaddr=0x100000 --patterntype=sha256 --patterndata=b3b7b5e5043302d1aa6f40af86fd0299a462cc8264fe1db58ac29218bae0984c --patternsha256size=0x40 "--plainout=#define IFile_Seek "' % (S1)
cmd(printstr)
if r:
	print("//WARNING: IFile_Seek not found.")