// kernel
#include <linux/kernel.h>
// pci driver
#include <linux/module.h>
#include <linux/pci.h>
// character device
#include <linux/device.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>

/***************************************************************************************************************/
/* Constants */
/***************************************************************************************************************/
#define PCI_CAPTURE_DRIVER "pci_capture_driver"             // name of PCI driver
#define PCI_CAPTURE_DRIVER_CHR_DEV "pci_capture_chr_dev"    // name of character device driver
#define MAJOR_NUMBER 0                                      // major number for character device
#define MAX_CHR_DEV 1                                       // amount of character devices
#define MAX_BUFFER_DATA_LEN (1920 * 1080 * 3)               // max length of buffer for a 1080p image (RGB)

/***************************************************************************************************************/
/* Driver functions */
/***************************************************************************************************************/

/* Generic functions to install/uninstall driver */
static int __init init_pci_capture_driver(void);
static void __exit finalize_pci_capture_driver(void);

/***************************************************************************************************************/
/* PCI driver */
/***************************************************************************************************************/

/* Functions for register/unregister PCI-Express driver */
static int register_pci_capture_device_driver(void);
static void unregister_pci_capture_device_driver(void);

/* Functions for install/uninstall PCI driver */
static int probe_pci_capture_driver(struct pci_dev *pdev, const struct pci_device_id *ent);
static void remove_pci_capture_driver(struct pci_dev *pdev);

// Vendor - Device
static struct pci_device_id pci_capture_driver_table[] = {
    {PCI_DEVICE(0x104C, 0xAC10)},
    {0,0}
};

/* PCI-Express Driver registration structure */
static struct pci_driver pci_capture_driver_registration = {
    .name = PCI_CAPTURE_DRIVER,
    .id_table = pci_capture_driver_table,
    .probe = probe_pci_capture_driver,
    .remove = remove_pci_capture_driver
};

/***************************************************************************************************************/
/* Character Device driver */
/***************************************************************************************************************/

/* Functions for install/uninstall character device driver */
static int register_pci_capture_chr_dev(void);
static void unregister_pci_capture_chr_dev(void);

/* Required functions for character device interaction */
static int open_pci_capture_chr_dev(struct inode *pinode, struct file *pfile);
static int close_pci_capture_chr_dev(struct inode *pinode, struct file *pfile);
static ssize_t read_pci_capture_chr_dev(struct file *pfile, char __user *buffer, size_t length, loff_t *offset);
static ssize_t write_pci_capture_chr_dev(struct file *pfile, const char __user *buffer, size_t length, loff_t *offset);

/* Character device registration structure */
static struct file_operations pci_capture_chr_dev_registration = {
    .owner = THIS_MODULE,
    .open = open_pci_capture_chr_dev,
    .release = close_pci_capture_chr_dev,
    .read = read_pci_capture_chr_dev,
    .write = write_pci_capture_chr_dev,
};

/***************************************************************************************************************/
/* Global variables */
/***************************************************************************************************************/
/* Structure to manage character device internal data */
struct character_device_internal_data {
    struct cdev cdev;
};

struct pci_dev *pci_dev;
static int dev_major = MAJOR_NUMBER;
static struct class *character_device_class = NULL;
static char image_buffer[MAX_BUFFER_DATA_LEN];  // Buffer to store the image

/* Declare an array to store the internal data for character devices */
static struct character_device_internal_data chr_dev_data[MAX_CHR_DEV];  // Correction: Now declared globally

/***************************************************************************************************************/
/* Functions definitions */
/***************************************************************************************************************/

/* Register drivers */
static int __init init_pci_capture_driver(void) {
    int error = 0;

    /* Try register PCI-Express driver */
    error = register_pci_capture_device_driver();
    if (error != 0) {
        printk("Cannot register PCI-Express driver for PCI_CAPTURE device");
        goto cannot_enable;
    }

    /* Try register character device driver */
    error = register_pci_capture_chr_dev();
    if (error < 0) {
        printk("Cannot register character device for PCI_CAPTURE device");
        goto chr_dev_failed;
    }

    /* If everything is OK */
    return 0;

chr_dev_failed:
    unregister_pci_capture_device_driver();
cannot_enable:
    return error;
}

/* Unregister drivers */
static void __exit finalize_pci_capture_driver(void) {
    unregister_pci_capture_chr_dev();
    unregister_pci_capture_device_driver();
}

static int register_pci_capture_device_driver(void) {
    /* Register new PCI-Express driver on the system */
    return pci_register_driver(&pci_capture_driver_registration);
}

static int register_pci_capture_chr_dev(void) {
    /* Register new character device on the system */
    int error, i;
    dev_t dev;
    const char *chr_dev_name = PCI_CAPTURE_DRIVER_CHR_DEV;

    error = alloc_chrdev_region(&dev, 0, MAX_CHR_DEV, chr_dev_name);
    
    dev_major = MAJOR(dev);
    
    character_device_class = class_create(THIS_MODULE, chr_dev_name);

    for (i = 0; i < MAX_CHR_DEV; i++) {
        cdev_init(&chr_dev_data[i].cdev, &pci_capture_chr_dev_registration);  // Now chr_dev_data[i] is properly declared
        chr_dev_data[i].cdev.owner = THIS_MODULE;

        cdev_add(&chr_dev_data[i].cdev, MKDEV(dev_major, i), 1);

        device_create(character_device_class, NULL, MKDEV(dev_major, i), NULL, "pci_capture_chr_dev-%d", i);
    }

    return 0;
}

static void unregister_pci_capture_device_driver(void) {
    /* Unregister PCI-Express driver */
    pci_unregister_driver(&pci_capture_driver_registration);
}

static void unregister_pci_capture_chr_dev(void) {
    /* Unregister character device */
    int i;

    for (i = 0; i < MAX_CHR_DEV; i++) {
        device_destroy(character_device_class, MKDEV(dev_major, i));
    }

    class_unregister(character_device_class);
    class_destroy(character_device_class);

    unregister_chrdev_region(MKDEV(dev_major, 0), MINORMASK);
}

/***************************************************************************************************************/
/* Function for enabling PCI-Express driver */
/***************************************************************************************************************/
static int probe_pci_capture_driver(struct pci_dev *pdev, const struct pci_device_id *ent) {
    int error;
    unsigned long mmio_start, mmio_len;

    /* Enable PCI-Express device */
    error = pci_enable_device(pdev);
    if (error != 0) {
        printk("Failed while enabling PCI-Express device. Error: %d\n", error);
        return error;
    }

    /* Request memory region for the BAR */
    error = pci_request_regions(pdev, PCI_CAPTURE_DRIVER);
    if (error != 0) {
        printk("Failed while requesting BAR regions PCI-Express device. Error: %d\n", error);
        pci_disable_device(pdev);
        return error;
    }

    /* Get start and stop memory offsets for BAR0 */
    mmio_start = pci_resource_start(pdev, 0);
    mmio_len = pci_resource_len(pdev, 0);

    printk("PCI_CAPTURE device BAR0: start at 0x%lx with length %lu\n", mmio_start, mmio_len);

    pci_dev = pdev;

    return 0;
}

/***************************************************************************************************************/
/* Function for disabling PCI-Express driver */
/***************************************************************************************************************/
static void remove_pci_capture_driver(struct pci_dev *pdev) {
    pci_release_regions(pdev);
    pci_disable_device(pdev);
}

/***************************************************************************************************************/
/* Character device file operations */
/***************************************************************************************************************/

/* Open character device */
static int open_pci_capture_chr_dev(struct inode *pinode, struct file *pfile) {
    printk("Character device file opened\n");
    return 0;
}

/* Close character device */
static int close_pci_capture_chr_dev(struct inode *pinode, struct file *pfile) {
    printk("Character device file closed\n");
    return 0;
}

/* Read image from the device to user space */
static ssize_t read_pci_capture_chr_dev(struct file *pfile, char __user *buffer, size_t length, loff_t *offset) {
    size_t datalen = MAX_BUFFER_DATA_LEN;

    printk("Reading image from PCI device\n");

    /* Ensure we are not reading more data than available */
    if (length > datalen) {
        length = datalen;
    }

    /* Copy the image data to user space */
    if (copy_to_user(buffer, image_buffer, length)) {
        return -EFAULT;
    }

    return length;
}

/* Write image (after filtering) to the device */
static ssize_t write_pci_capture_chr_dev(struct file *pfile, const char __user *buffer, size_t length, loff_t *offset) {
    size_t n_copied;

    printk("Writing filtered image to PCI device\n");

    /* Ensure that we don't copy more data than the buffer size */
    if (length > MAX_BUFFER_DATA_LEN) {
        length = MAX_BUFFER_DATA_LEN;
    }

    /* Copy the filtered image data from user space to kernel space */
    n_copied = copy_from_user(image_buffer, buffer, length);

    if (n_copied != 0) {
        printk("Couldn't copy %zd bytes from the user\n", n_copied);
        return -EFAULT;
    }

    /* Here we would typically write the data to the PCI device hardware */
    /* This is left as a simulation step, depending on your actual hardware setup */

    return length;
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Daniel Brenes");
MODULE_DESCRIPTION("Driver PCIe para captura y escritura de imágenes");
MODULE_VERSION("1.0");

module_init(init_pci_capture_driver);
module_exit(finalize_pci_capture_driver);
