# Genomics-OS Target Builder User Manual

## Introduction

Genomics-OS Target Builder is a reproducible target definition generation system designed for targeted sequencing workflows.

The system transforms a user-supplied gene list into a fully traceable target definition artifact consisting of:

* MANE transcript selections
* CDS interval definitions
* BED files
* provenance metadata
* quality control summaries
* audit mappings
* checksums

The objective is reproducible and transparent target panel generation.

---

# Concepts

## Gene List

A gene list is the primary input.

Example:

```text
BRCA1
BRCA2
TP53
ATM
CHEK2
```

Each gene symbol is interpreted and resolved prior to target generation.

---

## Gene Resolution

The system normalizes gene symbols before transcript selection.

Example:

```text
FAM175A → ABRAXAS1
MRE11A  → MRE11
```

This process ensures compatibility with current Ensembl annotations.

The complete mapping is written to:

```text
gene_symbol_mapping.tsv
```

---

## MANE Transcript Policy

Target Builder uses:

```text
MANE Select
```

as the transcript selection strategy.

Only one transcript is selected per gene.

Benefits:

* standardized reporting
* clinical relevance
* reproducibility
* reduced ambiguity

---

## CDS Extraction

Coding sequence intervals are extracted from:

```text
Ensembl Release 115
GRCh38
```

Only CDS regions belonging to selected MANE transcripts are retained.

---

## BED Generation

Two BED files are generated.

### Gene-Labeled BED

File:

```text
targets.mane_cds.gene_labeled.bed
```

Contains:

```text
chromosome
start
end
gene
transcript
```

Example:

```text
17 43044284 43044413 BRCA1|ENST00000357654
```

---

### Panel Union BED

File:

```text
targets.mane_cds.panel_union.bed
```

Contains merged target intervals suitable for workflow consumption.

Example:

```text
17 43044284 43044413 PANEL_UNION
```

---

# Quality Control

Target Builder automatically generates:

```text
target_qc.json
```

This file records:

* requested genes
* resolved genes
* transcript counts
* interval counts
* target territory

Example:

```json
{
  "requested_gene_count": 10,
  "mane_transcript_count": 10
}
```

---

# Provenance

Target Builder captures generation metadata in:

```text
target_manifest.json
```

The manifest contains:

* genome build
* annotation release
* transcript policy
* selected transcripts
* generation parameters
* output locations
* QC summary

This enables exact regeneration of a target definition.

---

# Audit Trail

File:

```text
gene_symbol_mapping.tsv
```

Provides a complete record of:

```text
requested gene
resolved gene
selected transcript
```

Example:

```text
requested_gene resolved_gene transcript_id

FAM175A ABRAXAS1 ENST00000XXXX
```

---

# Checksums

File:

```text
SHA256SUMS.txt
```

Contains SHA256 checksums for all generated artifacts.

Example:

```text
ad0081ef...
target_manifest.json
```

Checksums support:

* artifact verification
* transfer validation
* reproducibility audits

---

# Running Target Builder

## Example

```bash
uv run target-builder build \
  --genes examples/hereditary_cancer.txt \
  --padding 10 \
  --outdir output/hereditary_cancer
```

---

# Output Structure

```text
output/

└── hereditary_cancer/
    ├── targets.mane_cds.gene_labeled.bed
    ├── targets.mane_cds.panel_union.bed
    ├── target_qc.json
    ├── target_manifest.json
    ├── gene_symbol_mapping.tsv
    └── SHA256SUMS.txt
```

---

# Architecture

The internal processing flow is:

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
QC Generation
    ↓
Manifest Generation
    ↓
Checksum Generation
```

---

# Integration with Genomics-OS

Target Builder is designed as a Genomics-OS artifact producer.

Future integration:

```text
Target Builder
    ↓
Target Definition Artifact
    ↓
Artifact Registry
    ↓
Somatic Workflow
```

The generated artifacts are intended to become first-class entities within the broader Genomics-OS ecosystem.
