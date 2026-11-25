+++
id = "hpc4wc"
order = 30
title = "MPI domain decomposition for a multi-GPU shallow-water solver"
summary = "Does the shape of the MPI subdomains matter? Five 16-GPU decompositions benchmarked on CSCS Santis, with a hand-written MPI layer."
type = "Team project (3)"
year = "2026"
tags = ["HPC", "MPI", "Multi-GPU", "Julia", "Domain decomposition"]

[[media]]
src = "assets/img/hpc4wc_time_per_iteration.png"
caption = "Median time per iteration for the five 16-rank topologies, split into kernel time and communication time."

[[media]]
src = "assets/img/hpc4wc_decompositions.png"
caption = "The five decompositions compared, from 1×16 strips to 16×1 columns, on the same 4:1 global grid."

[[links]]
label = "Report (PDF)"
url = "assets/pdf/hpc4wc_domain_decomposition_report.pdf"

[[links]]
label = "Code on GitHub"
url = "https://github.com/ragassler/HPC4WC_project3_domain_decomp"
+++
Work project for *High-Performance Computing for Weather and Climate*
(ETH Zurich), with Dennis Eberli and Timon Maeder.

**Abstract.** This project investigates how the shape of a two-dimensional MPI
domain decomposition affects the performance of a multi-GPU shallow-water
solver. The starting point is the Julia code from the project above, based on
`ParallelStencil.jl` and `ImplicitGlobalGrid.jl` (IGG). Using a fixed global
problem and a fixed number of GPUs, we compare decompositions ranging from
strongly elongated process grids to balanced layouts, and relate local
subdomain geometry, boundary-to-volume ratio and communication cost to the
achieved cell-update rate.

## What we did

- Reproduced the distributed-memory work that IGG hides (Cartesian topology,
  neighbours, halo exchange) **directly with MPI.jl**, so decomposition and
  communication are fully under our control.
- Simplified the physics so the benchmark isolates decomposition effects, and
  made grid size, topology, time steps, warm-up and repetitions configurable.
- Benchmarked all five 16-rank topologies on GPU nodes of **CSCS Santis**,
  with separate builds that time only the kernels or only the halo exchange.

## Findings

- Throughput differs by only **about 2%** across the five topologies.
- The ranking is the *opposite* of what a simple boundary-to-volume ratio
  predicts. The strip decompositions (16×1, 1×16) are fastest and the balanced
  4×4 layout is slowest. The number of MPI neighbours and the resulting
  communication pattern matter more than total halo volume.
- Communication takes **8–11%** of each iteration, while kernel time is
  constant across topologies.
- At large problem sizes the hand-written MPI layer matches the IGG version.
  It adds no significant overhead while giving transparent control.
