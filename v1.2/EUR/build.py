import os,sys

with open("3ds_ropkit/otherapp.bin","rb") as f:
	oapp=f.read()
	
with open("3ds_ropkit/ropkit.bin","rb") as f:
	ropkit=f.read()
	ropkit+=(b"\x00"*(0x400-len(ropkit)))

with open("307/boss/wTRu2!!!(`!!+s(@","rb+") as f:
	f.seek(0x1000-0xc)
	f.write(ropkit+oapp)
	