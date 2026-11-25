+++
id = "ra-solid-mechanics"
order = 20
title = "Finite-element data generation for solid mechanics"
summary = "Research assistantship: generating FEM training data for hyperelastic, elastoplastic and fracture problems, including shape-optimised geometries."
type = "Research assistant, ongoing"
year = "2026"
tags = ["FEM", "FEniCSx", "Shape optimisation", "Python", "HPC"]
note = "Unpublished research. The code and results are not public, so this is a conceptual summary."
+++
Machine-learning surrogates for solid mechanics are only as good as the data
they are trained on. In this research assistantship, I work on a
**FEniCSx-based pipeline** that produces such datasets automatically:

- random geometry and mesh generation,
- hyperelastic, elastoplastic and phase-field fracture simulations,
- batch runs on the Euler cluster, with tested, linted and CI-checked code.

My current focus is **shape-optimised data generation**. Random geometries
rarely produce the "hard" cases a surrogate struggles with. Instead, the
geometry becomes an unknown that is optimised:

1. Describe the geometry as a displacement field on a fixed reference mesh
   and pull the mechanics problem back to that mesh, so the geometry can
   change without remeshing.
2. Compute **adjoint shape gradients** of a target quantity, checked with
   Taylor tests.
3. Run a smoothed gradient-based optimiser with exact checks that the mesh
   never folds, then compare optimised samples against random ones.
