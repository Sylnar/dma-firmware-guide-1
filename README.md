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

## Companion tool: NexusForge

[NexusForge](https://github.com/NexusForge-dev/NexusForge) is the Windows GUI
flasher this guide recommends. It bundles OpenOCD plus the CH347 driver and
handles board detection, DNA read, and SPI flash write in one click. Use it
instead of raw OpenOCD or vendor CLIs.

## Community

Join the Nexus Discord for questions, build help, and future revisions:

**[discord.gg/y49jPf8T5z](https://discord.gg/y49jPf8T5z)**

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
