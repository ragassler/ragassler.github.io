+++
id = "asl-social-force"
order = 40
title = "A performance-oriented implementation of the Social Force Model"
summary = "Single-core optimisation of a pedestrian simulation in C++ with AVX2: 21.8× faster than the baseline, 45% of SIMD FMA peak."
type = "Team project (4)"
year = "2026"
tags = ["HPC", "Performance engineering", "SIMD (AVX2)", "C++", "Roofline"]

[[media]]
src = "assets/media/asl_pedestrians.mp4"
caption = "Pedestrians in a corridor simulated with the Social Force Model, coloured by speed."

[[media]]
src = "assets/img/asl_performance.png"
caption = "Performance in flops/cycle against the number of pedestrians: the final AVX2 version reaches about 15 flops/cycle, compared with about 1 for the baseline."

[[links]]
label = "Report (PDF)"
url = "assets/pdf/asl_social_force_report.pdf"
+++
Final project for *Advanced Systems Lab* (ETH Zurich), with Jiri Käser,
Mathieu Martin and Noah Rutz.

**Abstract.** This report presents a performance-oriented implementation of
the Social Force Model in C++. The model is dominated by pairwise pedestrian
interactions, which makes it well suited for studying algorithmic structure,
instruction-level parallelism and SIMD vectorisation. Starting from a readable
baseline, the optimisation follows the main bottlenecks of the model: data
layout, redundant computations, expensive mathematical functions and the
quadratic interaction loop. The final implementation targets x86 with **AVX2
intrinsics**. Costly operations such as the exponential, reciprocal and
inverse square root are replaced by fast approximations, and the computation
moves from double to single precision. This is a deliberate speed–accuracy
trade-off, so the central question is where large gains are possible while
keeping the loss of accuracy small enough to preserve the simulation. The
fastest AVX2 version achieves a **speed-up of up to 21.8×** over the baseline
and reaches about **45.1% of the theoretical SIMD FMA peak**.
