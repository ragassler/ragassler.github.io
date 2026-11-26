+++
# Kept general on purpose: no model equations or method details of ZRM.
id = "semester-thesis"
order = 45
title = "FEM simulation of the ZRM viscoelastic model for different channel geometries"
summary = "Semester thesis: implementing a viscoelastic constitutive model in a finite-element framework and testing it from benchmark flows to 3D extrusion geometries."
type = "MSc semester thesis"
year = "2026"
tags = ["FEM", "COMSOL", "Viscoelastic flow", "Non-Newtonian fluids"]
note = "The thesis itself is not public. This is a general summary of the work."

[[media]]
src = "assets/img/semester_3d_wi_final.png"
caption = "Weissenberg number (Wi) at the final time in a 3D extrusion geometry. Wi is monitored to check the stability of the viscoelastic solve and shows where mesh refinement helps."
+++
Many industrial materials, such as polymer melts, pastes and other complex fluids,
are **viscoelastic**: they flow like a liquid but also store and release elastic
stress. Simulating them requires constitutive models that go beyond Newtonian
fluids, and these models are numerically demanding.

In this semester thesis I simulated a viscoelastic constitutive model with the
**finite element method** in channel geometries of increasing complexity.

- **Implementation:** set up and extended a viscoelastic flow model in COMSOL,
  including custom modifications of the constitutive equations.
- **Validation** on canonical benchmark flows (2D Couette and Poiseuille flow)
  before moving to complex geometries.
- **Application** to 2D and 3D extrusion-like channel geometries, analysing
  velocity fields, stress distributions and dissipation.
- **Physical consistency checks:** mass balance, energy and dissipation budgets,
  and the numerical robustness of the simulations across geometries.
