# Genomics-OS Target Builder

A small, reproducible target BED generation module for Genomics-OS.

V1 goal:

- accept a gene list
- resolve gene aliases
- extract CDS intervals from Ensembl GTF
- generate gene-labeled and panel-union BED files
- emit QC, checksums, and provenance manifest
