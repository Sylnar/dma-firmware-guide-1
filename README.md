# PCIe DMA Firmware Engineering Guide

A practical engineering reference for building 1:1 device emulation firmware on
Artix-7 FPGAs. Covers configuration space, capability chains, BDF stability,
MSI cadence, IOMMU realities, AHCI / SATA emulation, the Windows storage stack
walls, Vivado build reality, per-board identity, flashing, and live verification.

Vendor-agnostic. No proprietary code. No anti-cheat specifics. Provided as
engineering reference for educational and research use.

## Download

**[Download the latest guide (PDF)](Nexus_DMA_Firmware_Guide.pdf?raw=true)**

Direct link, no signup required.

## What is in the guide

56 pages covering:

- Hardware platform and toolchain (Vivado, Python, NexusForge, JTAG)
- The donor concept (what to buy, what to avoid, Arbor + lspci capture)
- Configuration space and capability chains
- BDF stability and the heartbeat tell
- MSI behavior
- IOMMU realities (the Hyper-V / VBS / KDP chain)
- AHCI / SATA emulation
- ATA command engine architecture
- Disk image, filesystem, and the partmgr wall
- Writes and persistence
- SystemVerilog pitfalls
- Vivado build reality
- Per-board identity (DNA binding)
- Flashing and deployment
- Live verification probes
- Common errors and diagnostics (Appendix A)
- Reading list (Appendix B)
- Glossary (Appendix C)
- A Quick Start "first build, step by step" section for beginners

## Who is this for

Engineers who already know HDL, Vivado, and PCIe at the spec level and want a
consolidated reference for the non-obvious problems that only show up after
weeks of hands-on work: silent multi-driver synthesis bugs, transient BDF
events, partmgr's hardcoded LBA 2 read, fastfat's directory-corruption rules,
the difference between IOMMU presence and IOMMU enforcement.

If you do not know what a TLP, BAR, or capability pointer is, read the PCIe
Base Specification first.

## Companion tool: Sylnar Tool

[Sylnar Tool](https://sylnar.com/sylnar-tool) is the Windows GUI for FPGA DMA
board management. It detects boards, reads Device DNA, installs CH347 and FT601
drivers, flashes firmware, and tests DMA speed. Download it from the
[official NexusForge releases](https://github.com/NexusForge-dev/NexusForge/releases/latest).

## Companion web guides

The [DMA firmware guide collection](https://nexusforge-dev.github.io/dma-firmware-guide/)
includes focused, linkable references for:

- [Artix-7 DMA firmware compatibility and flashing](https://nexusforge-dev.github.io/dma-firmware-guide/artix-7-dma-firmware.html)
- [Sylnar Tool board management](https://nexusforge-dev.github.io/dma-firmware-guide/sylnar-tool-guide.html)
- [Second-PC DMA setup](https://nexusforge-dev.github.io/dma-firmware-guide/second-pc-dma-setup.html)
- [CS2 DMA cheats and ESP](https://nexusforge-dev.github.io/dma-firmware-guide/cs2-dma-cheats.html)
- [Wardogs ESP and DMA overlay](https://nexusforge-dev.github.io/dma-firmware-guide/wardogs-esp-guide.html)

Current Sylnar resources:

- [SylnarCore Artix-7 DMA firmware](https://sylnar.com/sylnarcore)
- [Sylnar CS2 cheats and ESP](https://sylnar.com/cs2)
- [Sylnar Wardogs ESP](https://sylnar.com/wardogs)
- [DMA board and BIOS compatibility](https://sylnar.com/compatibility)

## Community

Join Sylnar on Discord for questions, build help, and future revisions:

**[discord.gg/sylnar](https://discord.gg/sylnar)**

## Updates

Open this repository's Releases page (or watch it on GitHub) to be notified
when a new revision of the guide is published.

## Disclaimer

The guide is provided for educational and research purposes only. The author
makes no warranty and accepts no liability for any use of the techniques
described. The full disclaimer is on the second page of the PDF and applies to
any use of this material. Redistribution and modification of the PDF is
permitted for non-commercial purposes provided the disclaimer remains attached.
Commercial redistribution requires prior written consent of the author.
