+++
id = "dphpc-spgemm"
order = 60
title = "Distributed symbolic sparse matrix–matrix multiplication"
summary = "Computing the sparsity pattern of C = A·B across MPI ranks while sending as little data as possible."
type = "Team project (5)"
year = "2023"
tags = ["HPC", "MPI", "Sparse linear algebra", "C++"]

# Add the report once it is in assets/pdf/:
# [[links]]
# label = "Report (PDF)"
# url = "assets/pdf/dphpc_symbolic_spgemm_report.pdf"
+++
Project for *Design of Parallel and High-Performance Computing* (ETH Zurich).
Sparse matrix–matrix multiplication (SpGEMM) is a key kernel in graph
analytics and multigrid solvers. Its **symbolic phase** determines the
sparsity pattern of the result, so that memory can be allocated before any
numbers are computed.

We implemented a distributed symbolic SpGEMM in C++ and MPI and compared
strategies for getting the needed columns of *B* to each rank:

- **broadcast** of every column by its owner,
- **all-gather** of all local columns,
- an **optimised all-to-all** where each rank requests only the columns it needs.
  The requests are encoded as merged vectors, sets or a compact **Bloom filter**.

Row/column overlap tests were vectorised with **AVX**. The code was built
with Meson, unit-tested with GoogleTest and benchmarked on the Euler cluster.
