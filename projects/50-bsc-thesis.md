+++
id = "bsc-thesis"
order = 50
title = "A well-balanced finite-volume approach to near-steady-state Euler equations"
summary = "Bachelor thesis: why standard schemes fail to keep equilibria, and what changes when well-balanced schemes go from 1D to 2D."
type = "BSc thesis"
year = "2024"
tags = ["FVM", "Well-balanced schemes", "Euler equations", "Numerical analysis"]
note = "Supervised by Dr. R. Käppeli, Seminar for Applied Mathematics, ETH Zurich."

[[media]]
src = "assets/img/bsc_wb_perturbation.png"
caption = "A small perturbation of a hydrostatic equilibrium. The well-balanced scheme (blue) resolves it cleanly. The standard scheme (red) is polluted by its own discretisation error."

[[links]]
label = "Read the thesis (PDF)"
url = "assets/pdf/bsc_thesis_gassler.pdf"
+++
**Abstract.** This thesis focuses on numerically solving (near) steady-state
Euler equations in 1D and 2D using standard Finite Volume Methods (FVM) and
Well-Balanced (WB) methods. It shows the problems that standard schemes face
in preserving steady states and explores the difficulties of extending WB
schemes directly into multidimensional settings. By comparing standard FVM with
WB methods, it highlights the benefits and limitations of each approach for
maintaining equilibrium states of the Euler equations in one and several
dimensions.

Topics include first- and second-order reconstructions, hydrostatic
equilibria under gravity, convergence studies, shock tubes and a
Rayleigh–Taylor instability test.
