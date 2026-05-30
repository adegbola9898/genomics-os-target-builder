# Genomics-OS Target Builder Developer Guide

## Purpose

This document explains the internal architecture of Genomics-OS Target Builder and provides guidance for future development.

The intended audience is developers extending or maintaining the project.

---

# Project Goal

Target Builder converts a gene list into a reproducible target definition artifact.

The system:

* resolves gene aliases
* selects MANE transcripts
* extracts CDS intervals
* generates BED outputs
* records provenance
* generates QC metrics
* produces audit mappings
* generates checksums

The repository serves as a reference implementation of artifact-centric computation within the Genomics-OS ecosystem.

---

# Design Principles

## Reproducibility First

Every generated target definition must be reproducible.

All outputs should be traceable to:

* genome build
* annotation release
* transcript selection policy
* generation parameters

---

## Explicit Provenance

Target definitions are treated as computational artifacts.

Every artifact should be accompanied by:

* metadata
* checksums
* lineage information

---

## Simplicity Before Abstraction

Avoid introducing frameworks or complex abstractions prematurely.

Current implementation favors:

* plain Python
* explicit functions
* straightforward data flow

over extensive object hierarchies.

---

# Repository Structure

```text
src/
└── target_builder/

    resolver.py
    transcript_selector.py
    gtf_extract.py
    bed_ops.py
    qc.py
    manifest.py
    checksums.py
    cli.py
```

---

# Module Responsibilities

## resolver.py

Purpose:

Gene alias normalization.

Example:

```text
FAM175A → ABRAXAS1
MRE11A → MRE11
```

Responsibilities:

* normalize symbols
* apply alias mappings

Future:

* HGNC integration
* alias database support

---

## transcript_selector.py

Purpose:

Select MANE transcripts.

Current policy:

```text
MANE_SELECT
```

Responsibilities:

* parse transcript metadata
* identify MANE transcripts
* map gene → transcript

Future:

* MANE Plus Clinical
* canonical transcript policies
* custom transcript policies

---

## gtf_extract.py

Purpose:

Extract CDS intervals from Ensembl GTF files.

Responsibilities:

* parse GTF records
* identify CDS features
* emit genomic intervals

Output:

```python
(
    chromosome,
    start,
    end,
    gene,
    transcript_id,
)
```

---

## bed_ops.py

Purpose:

BED interval manipulation.

Responsibilities:

* sorting
* merging
* interval padding
* panel union generation
* FAI boundary enforcement

This module should remain independent of transcript logic.

---

## qc.py

Purpose:

Generate quality-control summaries.

Current metrics:

* gene counts
* transcript counts
* interval counts
* target territory

Future metrics:

* exon counts
* transcript coverage summaries
* interval distribution statistics

---

## manifest.py

Purpose:

Generate provenance manifests.

Responsibilities:

* capture generation metadata
* record reference information
* record transcript selections
* embed QC results

The manifest is the primary provenance document.

---

## checksums.py

Purpose:

Generate artifact checksums.

Current algorithm:

```text
SHA256
```

Responsibilities:

* file hashing
* checksum manifest generation

---

## cli.py

Purpose:

Application entry point.

Responsibilities:

* argument parsing
* pipeline orchestration
* output generation

Current command:

```bash
target-builder build
```

Future commands:

```bash
target-builder inspect
target-builder validate
target-builder manifest
```

---

# Data Flow

The processing pipeline is:

```text
Gene List
    ↓
Alias Resolution
    ↓
MANE Transcript Selection
    ↓
CDS Extraction
    ↓
Interval Processing
    ↓
BED Generation
    ↓
QC Generation
    ↓
Manifest Generation
    ↓
Checksum Generation
```

---

# Generated Artifacts

Current outputs:

```text
targets.mane_cds.gene_labeled.bed
targets.mane_cds.panel_union.bed
target_qc.json
target_manifest.json
gene_symbol_mapping.tsv
SHA256SUMS.txt
```

These outputs collectively represent a target definition artifact.

---

# Testing Strategy

Current framework:

```text
pytest
```

Principles:

* test biological logic
* test interval operations
* test provenance generation
* test checksum generation

New functionality should include tests before merge.

---

# Reference Data

Current reference bundle:

```text
GRCh38
Ensembl 115
```

Development uses local symlinks:

```text
references/grch38/
```

These references are intentionally excluded from version control.

---

# Future Development

## Near-Term

* artifact contract generation
* artifact schema validation
* richer provenance metadata

## Medium-Term

* Genomics-OS integration
* artifact registry compatibility
* workflow consumption

## Long-Term

* multiple transcript policies
* additional genome builds
* non-coding target support
* panel design extensions

---

# Relationship to Genomics-OS

Target Builder is an artifact producer.

Future architecture:

```text
Target Builder
    ↓
Target Definition Artifact
    ↓
Artifact Registry
    ↓
Workflow Runtime
    ↓
Somatic Analysis
```

The repository should remain focused on target generation and should not absorb workflow execution responsibilities.

---

# Contribution Philosophy

When extending the repository:

1. preserve reproducibility
2. preserve provenance
3. add tests
4. keep biological assumptions explicit
5. avoid unnecessary abstractions

Target Builder should remain small, predictable, and biologically transparent.
