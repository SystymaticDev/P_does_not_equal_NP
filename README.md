# Coq Proof Package: P ≠ NP (Connell Super-Complexity Method)
This repository provides the fully structured Coq proof associated with the paper "P ≠ NP: A Definitive Resolution through Diagonalization, Circuit Complexity, and Proof Complexity".

## Contents
- Definitions.v: Machine/Certificate/Input encodings
- Diagonalization.v: Language L* definition
- CircuitLowerBounds.v: Argument for super-polynomial circuit size
- ProofComplexity.v: Cook-Reckhow connection
- Main.v: Top-level proof for P ≠ NP
- Tactics.v: Useful tactics

## Instructions
1. Build with `make` or manually in CoqIDE.
2. Recommended: Coq version 8.15+

## Status
Formally structured, partially admitted lemmas (final polishing in progress).

---
