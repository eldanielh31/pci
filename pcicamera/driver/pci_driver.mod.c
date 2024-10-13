#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/export-internal.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

#ifdef CONFIG_UNWINDER_ORC
#include <asm/orc_header.h>
ORC_HEADER;
#endif

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xedc03953, "iounmap" },
	{ 0xd597abe0, "pci_select_bars" },
	{ 0xccb08fd, "pci_release_region" },
	{ 0xc6068552, "pci_disable_device" },
	{ 0x122c3a7e, "_printk" },
	{ 0xb01a6e1b, "pci_unregister_driver" },
	{ 0xd938049e, "pci_enable_device" },
	{ 0x7a61f742, "pci_request_region" },
	{ 0xde80cd09, "ioremap" },
	{ 0xbdfb6dbb, "__fentry__" },
	{ 0x794979f9, "__pci_register_driver" },
	{ 0x5b8239ca, "__x86_return_thunk" },
	{ 0xf079b8f9, "module_layout" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("pci:v0000104Cd0000AC10sv*sd*bc*sc*i*");

MODULE_INFO(srcversion, "C36AF37B8197CBF27BCC739");
