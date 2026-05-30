# Genomics-OS Target Builder

Reproducible MANE-based target BED generation for Genomics-OS.

## Overview

Genomics-OS Target Builder is a reproducible target definition generator for targeted sequencing workflows.

Given a list of genes, the tool:

* resolves gene aliases
* selects MANE transcripts
* extracts coding sequence (CDS) intervals from Ensembl annotations
* generates BED files suitable for targeted sequencing workflows
* emits provenance metadata
* generates quality-control summaries
* produces checksums and audit trails

The objective is to make target definitions reproducible, traceable, and portable across workflows.

---

## Why This Exists

Target panels are often distributed as BED files with little information about:

* transcript selection policy
* annotation release
* genome build
* gene alias resolution
* provenance

This makes reproduction difficult.

Target Builder treats a target panel as a first-class computational artifact and records the metadata required to reproduce it.

---

## Features

### Gene Resolution

Supports gene alias normalization.

Example:

| Requested | Resolved |
| --------- | -------- |
| FAM175A   | ABRAXAS1 |
| MRE11A    | MRE11    |

### Transcript Policy

Current policy:

```text
MANE Select
```

One MANE transcript is selected per gene.

### Annotation Source

Current reference:

```text
Ensembl Release 115
GRCh38
```

### BED Generation

Produces:

* gene-labeled BED
* panel-union BED

### Provenance

Captures:

* genome build
* annotation release
* transcript policy
* selected transcripts
* generation parameters

### Quality Control

Captures:

* gene counts
* interval counts
* target territory
* transcript coverage statistics

### Checksums

Generates SHA256 checksums for all emitted artifacts.

---

## Installation

### Clone

```bash
git clone git@github.com:adegbola9898/genomics-os-target-builder.git
cd genomics-os-target-builder
```

### Install UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Run

```bash
uv run target-builder --help
```

---

## Example

Gene list:

```text
BRCA1
BRCA2
TP53
ATM
CHEK2
```

Build:

```bash
uv run target-builder build \
  --genes examples/hereditary_cancer.txt \
  --padding 10 \
  --outdir output/hereditary_cancer
```

---

## Outputs

Example output directory:

```text
output/hereditary_cancer/

├── targets.mane_cds.gene_labeled.bed
├── targets.mane_cds.panel_union.bed
├── target_qc.json
├── target_manifest.json
├── gene_symbol_mapping.tsv
└── SHA256SUMS.txt
```

### target_manifest.json

Contains:

* genome build
* annotation release
* transcript selections
* output locations
* QC summary

### target_qc.json

Contains:

* requested genes
* resolved genes
* transcript counts
* interval counts
* target territory

### gene_symbol_mapping.tsv

Provides an audit trail from requested genes to resolved symbols and selected transcripts.

### SHA256SUMS.txt

Checksums for all generated artifacts.

---

## Architecture

```text
Gene List
    ↓
Alias Resolution
    ↓
MANE Transcript Selection
    ↓
CDS Extraction
    ↓
BED Processing
    ↓
Artifact Generation
    ↓
QC + Provenance + Checksums
```

---

## Relationship to Genomics-OS

Target Builder is an artifact producer within the Genomics-OS ecosystem.

Future workflow:

```text
Target Builder
    ↓
Target Definition Artifact
    ↓
Somatic Workflow
    ↓
Analysis Artifacts
    ↓
Reporting
```

The repository serves as the reference implementation for reproducible target definition generation within Genomics-OS.

---

## Current Status

MVP Complete

Implemented:

* MANE transcript selection
* CDS extraction
* BED generation
* QC generation
* provenance manifests
* checksum generation
* audit mappings

Future:

* artifact contracts
* registry integration
* Genomics-OS runtime integration

---

## License

MIT

