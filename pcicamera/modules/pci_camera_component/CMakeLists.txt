# © 2023 Intel Corporation

simics_add_module(pci_camera_component
  COMPONENTS pci_camera_component
  SOURCES pci_camera_component.py module_load.py
  SIMICS_API latest
)
