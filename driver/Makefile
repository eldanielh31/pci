CC = x86_64-linux-gnu-gcc-12
obj-m += pci_driver.o
KVERSION = $(shell uname -r)
KDIR = /lib/modules/$(KVERSION)/build

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

load:
	sudo insmod pci_driver.ko
# sudo chmod 666 /dev/arduino0

unload:
	sudo rmmod pci_driver

check:
	watch -n 2 lsusb -t

port:
	lsusb -v -d 2341:0043

kernel:
	sudo dmesg -w
