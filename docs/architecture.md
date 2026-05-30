# Genomics-OS Target Builder Architecture

## Purpose

Genomics-OS Target Builder is a specialized artifact-generation system within the broader Genomics-OS ecosystem.

Its responsibility is to transform biological target definitions into reproducible computational artifacts.

The repository intentionally focuses on target generation and does not perform workflow execution, variant calling, annotation, or reporting.

---

# Architectural Context

Genomics-OS is based on several core principles:

* artifact-centric computation
* provenance-native reproducibility
* structured scientific state
* portable execution
* searchable computational history

Target Builder exists to validate these principles in a focused biological domain.

---

# Problem Statement

Target panels are often represented as BED files with insufficient metadata.

Common missing information includes:

* transcript selection strategy
* annotation release
* genome build
* alias resolution decisions
* generation parameters

As a result, reproducing a target definition months or years later can be difficult.

Target Builder addresses this by treating target definitions as first-class computational artifacts.

---

# System Boundary

Target Builder is responsible for:

```text id="mvv06s"
Gene List
    ↓
Transcript Selection
    ↓
CDS Extraction
    ↓
BED Generation
    ↓
Artifact Generation
```

Target Builder is NOT responsible for:

```text id="zlb2l9"
Alignment
Variant Calling
Annotation
Reporting
Workflow Scheduling
Artifact Storage
```

Those responsibilities belong elsewhere in Genomics-OS.

---

# High-Level Architecture

```text id="q4dshw"
Input Layer
    ↓
Resolution Layer
    ↓
Transcript Layer
    ↓
Extraction Layer
    ↓
Interval Processing Layer
    ↓
Artifact Generation Layer
```

---

# Processing Pipeline

## Step 1: Gene Ingestion

Input:

```text id="7a5l7k"
BRCA1
BRCA2
TP53
```

The system loads user-specified gene symbols.

---

## Step 2: Alias Resolution

Responsibilities:

* symbol normalization
* alias correction

Example:

```text id="4vlx8m"
FAM175A → ABRAXAS1
```

Output:

```text id="9mhl1y"
resolved gene symbols
```

---

## Step 3: Transcript Selection

Current policy:

```text id="8j6l4u"
MANE Select
```

Responsibilities:

* identify MANE transcripts
* build gene → transcript mapping

Output:

```text id="bj15yo"
gene
↓
transcript
```

---

## Step 4: CDS Extraction

Source:

```text id="dd1s42"
Ensembl Release 115
GRCh38
```

Responsibilities:

* parse GTF
* identify CDS records
* extract intervals

Output:

```text id="j9e3lu"
chromosome
start
end
gene
transcript
```

---

## Step 5: Interval Processing

Responsibilities:

* sorting
* merging
* padding
* panel union generation
* boundary validation

Output:

```text id="qux4n6"
final target intervals
```

---

## Step 6: Artifact Generation

Outputs:

```text id="2brw0v"
targets.mane_cds.gene_labeled.bed
targets.mane_cds.panel_union.bed
target_qc.json
target_manifest.json
gene_symbol_mapping.tsv
SHA256SUMS.txt
```

These outputs collectively form a target definition artifact.

---

# Artifact-Centric Design

A central design goal is that every target definition becomes a reproducible artifact.

The artifact contains:

```text id="wkt8pk"
Biological Definition
+
Provenance
+
QC
+
Audit Trail
+
Checksums
```

rather than a BED file alone.

---

# Provenance Model

Target Builder records:

* genome build
* annotation release
* transcript policy
* selected transcripts
* generation parameters

This information is stored in:

```text id="wjnk4l"
target_manifest.json
```

The manifest serves as the authoritative provenance document.

---

# Audit Model

The repository records biological decision points.

Current example:

```text id="sxw3iy"
requested gene
↓
resolved gene
↓
selected transcript
```

Output:

```text id="c6f1dc"
gene_symbol_mapping.tsv
```

This allows future users to understand exactly how target definitions were generated.

---

# Quality Control Model

Quality control is generated automatically.

Current metrics:

* requested genes
* resolved genes
* transcript counts
* interval counts
* target territory

Output:

```text id="4jz2d4"
target_qc.json
```

---

# Integrity Model

Artifact integrity is validated through SHA256 checksums.

Output:

```text id="mvg6hl"
SHA256SUMS.txt
```

Checksums allow:

* verification
* transfer validation
* reproducibility audits

---

# Relationship to Genomics-OS

Target Builder is a producer within the Genomics-OS architecture.

Future integration:

```text id="w17a2n"
Target Builder
    ↓
Target Definition Artifact
    ↓
Artifact Registry
    ↓
Workflow Runtime
    ↓
Somatic Workflow
```

The repository intentionally remains independent of workflow execution.

---

# Future Artifact Contract

The long-term objective is to expose target definitions through a formal artifact contract.

Conceptually:

```json
{
  "artifact_type": "target_definition",
  "artifact_version": "1",
  "manifest": "...",
  "artifacts": [...],
  "checksums": "..."
}
```

This will allow seamless integration with future Genomics-OS services.

---

# Architectural Principles

Future development should preserve:

1. reproducibility
2. provenance
3. biological transparency
4. artifact-centric design
5. minimal complexity

Target Builder should remain a focused artifact producer rather than evolving into a workflow engine.

---

# Current Status

Version:

```text id="by4ffw"
MVP Complete
```

Implemented:

* MANE transcript selection
* CDS extraction
* BED generation
* QC generation
* provenance manifests
* audit mappings
* checksum generation

The repository serves as the first artifact producer within the Genomics-OS ecosystem and provides a reference implementation of artifact-centric biological computation.
