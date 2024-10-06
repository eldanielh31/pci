// Archivo: pci_driver.c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/pci.h>
#include <linux/interrupt.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "pci_example_driver"
#define PCI_VENDOR_ID_EXAMPLE 0x1234    // Reemplazar con el vendor ID de tu dispositivo
#define PCI_DEVICE_ID_EXAMPLE 0x5678    // Reemplazar con el device ID de tu dispositivo

// Estructura para el dispositivo PCI
struct pci_example_dev {
    struct pci_dev *pdev;
    void __iomem *hw_addr;
};

static struct pci_example_dev example_dev;

// Función de inicialización del driver PCIe
static int pci_example_probe(struct pci_dev *dev, const struct pci_device_id *id)
{
    int bar;
    int result;
    resource_size_t mmio_start, mmio_len;

    // Habilitar el dispositivo PCI
    result = pci_enable_device(dev);
    if (result) {
        printk(KERN_ERR "Cannot enable PCI device\n");
        return result;
    }

    // Obtener la dirección base del dispositivo (BAR)
    bar = pci_select_bars(dev, IORESOURCE_MEM);
    result = pci_request_region(dev, bar, DEVICE_NAME);
    if (result) {
        printk(KERN_ERR "Cannot request PCI region\n");
        pci_disable_device(dev);
        return result;
    }

    // Mapear el espacio de direcciones del dispositivo al kernel
    mmio_start = pci_resource_start(dev, 0);
    mmio_len = pci_resource_len(dev, 0);
    example_dev.hw_addr = ioremap(mmio_start, mmio_len);
    if (!example_dev.hw_addr) {
        printk(KERN_ERR "Cannot map PCI device to memory\n");
        pci_release_region(dev, bar);
        pci_disable_device(dev);
        return -ENOMEM;
    }

    example_dev.pdev = dev;
    printk(KERN_INFO "PCI device %s enabled and mapped at 0x%lx\n", DEVICE_NAME, (unsigned long)mmio_start);
    return 0;
}

// Función de limpieza del driver PCIe
static void pci_example_remove(struct pci_dev *dev)
{
    iounmap(example_dev.hw_addr);
    pci_release_region(dev, pci_select_bars(dev, IORESOURCE_MEM));
    pci_disable_device(dev);
    printk(KERN_INFO "PCI device removed\n");
}

// Tabla de identificación del dispositivo PCIe
static const struct pci_device_id pci_example_ids[] = {
    { PCI_DEVICE(PCI_VENDOR_ID_EXAMPLE, PCI_DEVICE_ID_EXAMPLE) },
    { 0, }
};

MODULE_DEVICE_TABLE(pci, pci_example_ids);

// Estructura del driver PCI
static struct pci_driver pci_example_driver = {
    .name = DEVICE_NAME,
    .id_table = pci_example_ids,
    .probe = pci_example_probe,
    .remove = pci_example_remove,
};

// Función de inicialización del módulo del kernel
static int __init pci_example_init(void)
{
    return pci_register_driver(&pci_example_driver);
}

// Función de salida del módulo del kernel
static void __exit pci_example_exit(void)
{
    pci_unregister_driver(&pci_example_driver);
}

module_init(pci_example_init);
module_exit(pci_example_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Daniel");
MODULE_DESCRIPTION("Driver PCIe de ejemplo para dispositivo virtual.");
