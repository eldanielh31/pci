# © 2023 Intel Corporation

simics_add_module(pci_camera
  CLASSES pci_camera
  SOURCES pci_camera.dml module_load.py
  SIMICS_API 6
)
add_subdirectory(test)
