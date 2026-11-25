+++
id = "hpc4wc"
order = 30
title = "Domain decomposition for a multi-GPU shallow-water solver"
summary = "How the shape of MPI subdomains affects halo-exchange cost and throughput on GPU nodes at CSCS."
type = "Team project"
year = "2026"
tags = ["HPC", "MPI", "Multi-GPU", "Julia", "Domain decomposition"]

[[media]]
src = "assets/img/hpc4wc_decompositions.png"
caption = "The five 16-rank decompositions compared, from 1×16 strips to 16×1 columns."

[[media]]
src = "assets/img/hpc4wc_strong_scaling.png"
caption = "Strong-scaling throughput from 2²⁰ to 2³² cells for the library baseline and each manual topology."

[[links]]
label = "Code on GitHub"
url = "https://github.com/ragassler/HPC4WC_project3_domain_decomp"
+++
Project for the block course *High-Performance Computing for Weather and
Climate* (ETH Zurich), done in a team of two. Starting from the shallow-water solver above,
we built a lean benchmark code and studied **how the domain is cut across
MPI ranks**.

- Two solver variants sharing the same `ParallelStencil.jl` kernels: a baseline
  using `ImplicitGlobalGrid.jl`, and a **hand-written MPI Cartesian
  decomposition** (`MPI.Cart_create`, blocking halo exchange).
- Rectangular topologies from 1×16 to 16×1 on the same global grid, which
  changes the halo surface each rank has to exchange.
- Separate timing builds isolate **kernel time** from **halo-exchange time**,
  so compute and communication costs can be compared directly.
- Strong-scaling sweeps over four orders of magnitude in problem size, run on
  GPU nodes at CSCS (Santis) with Slurm. Throughput saturates around
  40 GCell updates/s for large grids.
- Validation that both variants produce identical fields for every topology.
