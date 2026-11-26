+++
id = "dphpc-spgemm"
order = 60
title = "Communication-efficient symbolic SpGEMM on distributed memory"
summary = "Computing the sparsity pattern of C = A·B across MPI ranks while sending as few columns as possible, using Bloom filters."
type = "Team project (5)"
year = "2023"
tags = ["HPC", "MPI", "Sparse linear algebra", "C++"]

[[media]]
src = "assets/img/spgemm_bloom_filter.png"
caption = "Each rank encodes the row indices it needs in a Bloom filter. Other ranks then send only columns that hit the filter (false positives are possible, misses never)."

[[media]]
src = "assets/img/spgemm_overlap_methods.png"
caption = "Row/column overlap check: the hash-map approach is about 100× faster than moving pointers or binary search (random matrices, sparsity 10⁻⁴)."

[[links]]
label = "Report (PDF)"
url = "assets/pdf/dphpc_symbolic_spgemm_report.pdf"
+++
Project for *Design of Parallel and High-Performance Computing* (ETH Zurich),
with Diego de los Santos, Sascha Pucillo, Anirudhh Ramesh and Florence Kissling.
My focus was the **Bloom-filter** approach for deciding which columns each
rank actually needs.

Sparse general matrix–matrix multiplication (SpGEMM) is a key kernel in
graph analytics and multigrid solvers. Its **symbolic phase** determines the
sparsity pattern of the result before any values are computed. We parallelised
it on CPUs with MPI, with a focus on **reducing communication**.

## Approach

- Rows of *A* and columns of *B* are shuffled (to break up load-imbalancing
  patterns) and scattered across ranks with `MPI_Scatterv`.
- Three ways to share columns: broadcast, `MPI_Allgatherv` of everything, and
  an **optimised `MPI_Alltoallv`** that sends each rank only the columns it
  actually needs.
- The needed columns are found with merged row vectors, merged sets, or a
  compact **Bloom filter**, half the size of the merged set, with 11 hash functions.
- Four ways to test row/column overlap: binary search, moving pointers,
  AVX bit masks and a hash map.

## Results

- The hash-map overlap check was **about 100× faster** than moving pointers,
  and was the largest single gain.
- Optimised all-to-all with Bloom filter was the fastest communication
  scheme in most runs on the real matrices poli3 and lhr17. On lhr17, runtime
  halved with each doubling of processes up to 32.
- The final version was benchmarked against Eigen's sequential SpGEMM on six
  real-world matrices (up to 124 million non-zeros) on the Euler cluster,
  using up to 48 cores.
