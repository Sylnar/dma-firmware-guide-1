# Version 2.0 - 14 November 2026

Revised the public firmware engineering guide and added editable source, a
printable HTML edition and a reproducible PDF builder. Removed the version 1 PDF
and updated the download links to version 2. The original disclaimer wording is retained.

## Corrected

- Kernel DMA Protection and VBS are distinct; VBS is not a prerequisite.
- Board connector, transport and flash layout assumptions are board-specific.
- Reset and interrupt behavior must follow the implemented core and interface.
- Asymmetric FIFO depths must be reasoned about in terms of capacity and IP rules.
- Fixed small positive timing margins do not establish hardware stability.
- Unsupported operations must not be falsely acknowledged as successful.
- Stop codes and event IDs are diagnostic inputs, not unique root-cause proofs.
- Removed blanket host-protection changes, destructive cache cleanup and
  undocumented metadata workarounds from the recommended workflow.

## Added

- Explicit evidence labels and verification limits.
- DMA mapping lifetime, completion tracking and scatter/gather validation.
- CDC, reset, arbitration and backpressure review.
- Build manifests, running-build identification and rollback preparation.
- Read-only diagnostic examples and a release acceptance matrix.
- Public primary-source references and a practical support intake.

The existing game-related companion pages were left unchanged. This revision is
limited to the firmware engineering guide and its entry links.
