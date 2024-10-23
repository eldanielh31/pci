gcc
sudo swupd bundle-add linux-dev
sudo swupd bundle-add linux-dev
sudo swupd bundle-add linux-dev
uname -r
ls
mkdir driver
cd driver/
vim driver.c
ls
vim Makefile
mv driver.c test_pci.o
make

sudo swupd bundle-add gcc
gcc
sudo swupd bundle-add c-basic
make
vim Makefile 
ls
vim test_pci.o 
mv test_pci.o test_pci.c
make
sudo shutdown -r now
