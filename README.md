# PCIe DMA Firmware Engineering Guide - Version 2

A public engineering reference for developing and validating PCIe endpoints on
Artix-7 FPGA boards. Version 2 replaces unsupported generalizations with documented
behavior, explicit interface contracts and reproducible verification.

**Edition:** 2.0, revised 14 November 2026.

## Read the guide

- [Download version 2 (PDF)](Sylnar_DMA_Firmware_Guide_v2.pdf?raw=true)
- [Printable HTML edition](docs/firmware-guide-v2.html)
- [Editable guide source](guide/guide-v2.txt)
- [Version 2 changes](CHANGELOG.md)

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

The builder creates the PDF and `docs/firmware-guide-v2.html` from the editable
source. Windows Arial/Consolas fonts are used when available; portable standard
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
