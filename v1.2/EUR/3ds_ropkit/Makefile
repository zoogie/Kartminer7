HAXNAME := ropkit

all:	ropkit.bin

clean:
	rm -f $(HAXNAME).elf ropkit.bin

ropkit.bin: $(HAXNAME).elf
	arm-none-eabi-objcopy -O binary $(HAXNAME).elf ropkit.bin

$(HAXNAME).elf:	$(HAXNAME).s
	arm-none-eabi-gcc -x assembler-with-cpp -nostartfiles -nostdlib -Ttext=0x1579e600 $< -o $(HAXNAME).elf

