# PCIe DMA Firmware Engineering Guide - Version 2

A public engineering reference for developing and validating PCIe endpoints on
Artix-7 FPGA boards. Version 2 replaces unsupported generalizations with documented
behavior, explicit interface contracts and reproducible verification.

**Edition:** 2.1, revised 14 November 2026.

## Read the guide

- [Download version 2 (PDF)](Sylnar_DMA_Firmware_Guide_v2.pdf?raw=true)
- [Printable HTML edition](docs/firmware-guide-v2.html)
- [Editable guide source](guide/guide-v2.txt)
- [Step-by-step build and device-emulation labs](guide/hands-on.txt)
- [Complete register-device HDL, simulator testbench and Linux host tool](examples/register-lab/)
- [Version 2 changes](CHANGELOG.md)

**Community:** [Join the Sylnar Discord](https://discord.gg/sylnar).
The Discord link is also on the PDF cover, HTML header and guide's closing page.

## Build firmware and emulate a device

The guide now includes six hands-on labs: obtain and pin a public board project,
build its baseline, implement a register device, run its self-checking simulation,
integrate it into the PCIe project, build and program the image, and verify it from
the host. The reference-device workflow explains capture, interface specification,
configuration, register semantics, functional commands, interrupts, reset and
comparison testing. Complete teaching source is printed in the PDF as well as
included in `examples/register-lab`.

The original HDL example passed 56 local checks with Vivado Simulator 2022.2.
Full-board synthesis, programming and host acceptance have not been performed as
part of this documentation revision. The example uses a public upstream interface
and no private product implementation or hardware identity.

The version 1 PDF has been replaced by the version 2 download above.
The original disclaimer is retained, with its wording
unchanged, in both editions and in [the disclaimer source](guide/disclaimer.txt).

## Coverage

1. Scope and evidence: specified, implemented, simulated and hardware-verified.
2. Board identification, cabling, host/operator roles and recovery planning.
3. A controlled first-build and programming loop.
4. Configuration space and register contracts.
5. Capabilities, interrupts and power/reset behavior.
6. DMA addresses, mapping lifetime and IOMMU behavior.
7. Transaction tracking, scatter/gather and completion correctness.
8. HDL ownership, simultaneous updates, CDC and reset.
9. FIFO sizing, width conversion, arbitration and backpressure.
10. Public class-interface conformance and truthful completion semantics.
11. Reproducible Vivado builds and artifact manifests.
12. Timing constraints, implementation quality and acceptance.
13. Board-specific programming, running-build verification and rollback.
14. Read-only Windows and Linux diagnostics.
15. A hardware verification and release matrix.
16. Symptom-driven troubleshooting.
17. Compatibility and support intake.
18. Version 1 corrections, checklists, glossary and public primary references.

This guide describes general engineering practice. It does not disclose Sylnar's
private implementation, identify reference hardware, or certify compatibility for
a commercial product. Current support and commercial terms belong to the official
product documentation and private support process.

## Rebuild

Use a Python environment with the dependency in `scripts/requirements-guide.txt`:

```powershell
python -m pip install -r scripts/requirements-guide.txt
python scripts/build_guide.py
```

The builder creates the PDF and `docs/firmware-guide-v2.html` from both guide text
files and the included example code. Windows Arial/Consolas fonts are used when available; portable standard
PDF fonts are the fallback. PDF pagination can differ with the installed fonts.

## Official resources

- [Sylnar compatibility](https://sylnar.com/compatibility)
- [Sylnar Tool](https://sylnar.com/sylnar-tool)
- [Community and private support](https://sylnar.com/discord)

The existing short companion pages in `docs/` are separate from the version 2
firmware engineering guide.

## Distribution

The original disclaimer remains attached to the revised guide. Non-commercial
redistribution and modification are subject to that disclaimer; commercial
redistribution requires the author's prior written consent. Read the full
disclaimer in the guide.
