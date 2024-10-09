# © 2010 Intel Corporation

import cli
import pci_common


class_name = 'pci_camera'
"""
#
# ------------------------ info -----------------------
#

def get_info(obj):
    # USER-TODO: Return something useful here
    return []

cli.new_info_command(class_name, get_info)

#
# ------------------------ status -----------------------
#

def get_status(obj):
    # USER-TODO: Return something useful here
    return [("Registers",
             [("Counter", obj.regs_counter)])]

cli.new_status_command(class_name, get_status)
"""


cli.new_info_command("pci_camera", pci_common.get_pci_info)
cli.new_status_command("pci_camera", pci_common.get_pci_status)
pci_common.new_pci_config_regs_command('pci_camera', None)