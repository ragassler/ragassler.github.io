+++
id = "swe-gpu"
order = 10
title = "Shallow-water equations on multi-GPU, and the Cleuson dam break"
summary = "Well-balanced wet/dry finite-volume solver in Julia, from one GPU to 64, applied to a real Swiss dam-break scenario."
type = "Team project, then solo extension"
year = "2026"
tags = ["HPC", "FVM", "Multi-GPU", "Julia", "MPI", "Hydrodynamics"]

[[media]]
src = "assets/media/cleuson_section.mp4"
caption = "Free-surface profile through lake, dam and outlet, extracted from the 2D simulation, next to a map of water depth."

[[media]]
src = "assets/media/cleuson_valley_3d.mp4"
caption = "Flood wave from Lac de Cleuson down the Printze valley to Siviez. 5 m grid, 700 × 1500 cells, 200 s simulated."

[[media]]
src = "assets/img/swe_weak_scaling.png"
caption = "Weak scaling of the multi-GPU solver, 2000² cells per GPU."

[[media]]
src = "assets/media/swe_gauss_3d.mp4"
caption = "Wave propagation over topography, rendered from multi-GPU output."

[[links]]
label = "Code on GitHub"
url = "https://github.com/S1ntax3rror/ShallowWater4PDEonGPU"

[[links]]
label = "Final presentation (PDF)"
url = "assets/pdf/swe_multi_gpu_slides.pdf"
+++
The **shallow-water equations** describe free-surface flows such as tsunamis,
floods and dam breaks. They are hard to solve because of wet/dry fronts,
steady states over uneven terrain that must be preserved exactly, and the very
large grids that realistic terrain requires.

## Team phase: a portable multi-GPU solver

This started as the final project of *Solving PDEs in Parallel on GPUs II*
(ETH Zurich), together with Jiri Käser. We wrote a 2D solver in Julia that runs
from **one code base on a CPU, a single GPU or many GPUs**:

- first-order finite-volume scheme with Rusanov fluxes and bottom topography,
- **well-balanced hydrostatic reconstruction**, so a lake at rest stays exactly at rest,
- wet/dry stabilisation and absorbing sponge layers,
- `ParallelStencil.jl` kernels for CPU/GPU portability and `ImplicitGlobalGrid.jl`
  for MPI domain decomposition with halo exchange,
- memory-throughput analysis and weak scaling up to 64 GPUs: almost perfect up
  to 8 GPUs and 1.25× runtime at 64, with an unexplained outlier at 32.

## Solo extension: the Cleuson dam break

I then completed the wet/dry treatment and built a realistic test case on my
own. It uses Lac de Cleuson (Valais) on **real swissALTI3D terrain**: the lake starts at rest,
the dam is removed after 30 s, and the flood wave runs down the valley through Siviez.

- Terrain pipeline: 32 swisstopo tiles at 2 m, resampled to 25 m, 5 m or 2.5 m grids.
  The lake outline comes from the FOEN lake inventory. The lake bed is idealised.
- Manning bed friction, radiative boundaries, CFL 0.45.
- Built-in verification: the intact lake shows *zero* change in depth or
  momentum, depths stay non-negative, and the full-domain mass balance
  (including outflow) closes to a relative error of about 10⁻¹⁴.
- The 5 m run (8723 time steps) took 21 minutes on four CPU threads.
- Scientific visualisation: 3D oblique views, top-down depth maps and a
  longitudinal free-surface section, all sharing one fixed colour scale.
