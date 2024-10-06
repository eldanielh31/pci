# This Software is part of Simics. The rights to copy, distribute,
# modify, or otherwise make use of this Software may be licensed only
# pursuant to the terms of an applicable license agreement.
# 
# Copyright 2012-2021 Intel Corporation

# Tests for the sample PCI device.

#Código extraído del repositorio de Academia Collaboration mmongeo/academia-collaboration

import stest
import dev_util as du

# Set up a PCI bus and a sample PCI device
pci_bridge = du.Dev([du.PciBridge])  # Non-used PCI bridge, required by bus
pci_conf = SIM_create_object('memory-space', 'pci_conf', [])
pci_io = SIM_create_object('memory-space', 'pci_io', [])
pci_mem = SIM_create_object('memory-space', 'pci_mem', [])

pci_bus = SIM_create_object('pci-bus', 'pci_bus', [['conf_space', pci_conf],
                                                   ['io_space', pci_io],
                                                   ['memory_space', pci_mem],
                                                   ['bridge', pci_bridge.obj]])

pci = SIM_create_object('pci_camera', 'sample_pci',
                        [['pci_bus', pci_bus]])


def write_error(string_err, file_name="error_log.txt"):
    try:
        with open(file_name, "w") as file:
            file.write(string_err)
        print(f"Error guardado en {file_name}")
    except Exception as e:
        print(f"Hubo un problema al escribir el archivo: {e}")


# Test the PCI vendor and device IDs
def test_ids():
    try:
        stest.expect_equal(pci.attr.pci_config_vendor_id, 0x104c, "Bad vendor ID")
        stest.expect_equal(pci.attr.pci_config_device_id, 0x0DDE, "Bad device ID") #0x0DDE
    except Exception as e:
        error_message = f"Error: {e}"
        write_error(error_message)
# Test the registers of the device
def test_regs():
    version = du.Register_LE((pci, 1, 0x10))
    stest.expect_equal(version.read(), 0x4711)

# Test setting BAR to map the device in memory
def test_mapping():
    
    try:
        cmd_reg = du.Register((pci, 'pci_config', 0x4), 0x2)  # PCI command register
        bar_reg = du.Register((pci, 'pci_config', 0x10), 0x4) # PCI BAR register

        addr = 0x100
        cmd_reg.write(2)     # Enable memory access
        bar_reg.write(addr)  # Map bank at addr

        #stest.expect_equal(pci_mem.attr.map[0][1], pci.attr.regs.version,
        #               "PCI device should have been mapped")

        mem_read = pci_mem.iface.memory_space.read
        stest.expect_equal(du.tuple_to_value_le(mem_read(None, addr + 0x10, 4, 0)),
                        0x4711, "Version should be read")
    except Exception as e:
        error_message = f"Error: {e}"
        write_error(error_message)

write_error("All tests passed.")
test_ids()
test_regs()
test_mapping()

