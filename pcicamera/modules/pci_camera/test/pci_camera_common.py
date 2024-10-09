# © 2010 Intel Corporation

import simics

# Extend this function if your device requires any additional attributes to be
# set. It is often sensible to make additional arguments to this function
# optional, and let the function create mock objects if needed.
def create_pci_camera(name = None):
    '''Create a new pci_camera object'''
    pci_camera = simics.pre_conf_object(name, 'pci_camera')
    simics.SIM_add_configuration([pci_camera], None)
    return simics.SIM_get_object(pci_camera.name)
