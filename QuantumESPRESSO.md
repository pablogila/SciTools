# Quantum ESPRESSO

[Quantum ESPRESSO](https://www.quantum-espresso.org/) is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials modeling at the nanoscale. It is based on density-functional theory, plane waves, and pseudopotentials. It is preinstalled in Atlas & Hyperion.

## Inputs

It is useful to follow a custom [[Naming conventions#For calculations|naming convention]] for the calculations, as
`MATERIAL_yyMMddx_CALCULATION_EXTRA`
eg.
`MAPI-ND-5_240729a_relax_test`

PWsfc pw.x inputs need a `filename.in`, called by a Slurm file.
Check the syntax of the input in [Quantum ESPRESSO input data description](https://www.quantum-espresso.org/documentation/input-data-description/)

Energy units are in *Rydbergs*, and distance units in *bohrs*, unless stated otherwise.

We should write exponentials with double precision, with `d` instead of `e`, as in `conv_thr = 1.47d-12`

Semiconductors are treated as insulators, so that `occupations=fixed`.

Sometimes the slurm output may indicate floating point exceptions as below, which is [irrelevant](https://lists.quantum-espresso.org/pipermail/users/2019-October/043476.html)
```
NOTE: The following floating-point exceptions are signalling: IEEE_UNDERFLOW_FLAG IEEE_DENORMAL
```

isotopes in the [ATOMIC_SPECIES](https://www.quantum-espresso.org/Doc/INPUT_PW.html#ATOMIC_SPECIES) must start by the actual letter from the species, such as H2; It can not be D.

To export to a .CIF file after the calculation, we can use [[ASE#Exporting outputs|ASE]]. The graphical option would be to open the output on XCrySDen and save it as `.xsf`, then open it on [VESTA](https://jp-minerals.org/vesta/en/) and save it as `.cif`. This last option seems to preserve a bit better the numerical precision, since both [ASE](ASE.md) and [VESTA](https://jp-minerals.org/vesta/en/) cut some decimals for some weird reason.

## Crystal structure

In Quantum Espresso, the structure information is provided by `ibrav` number, and corresponding `celldm` values or lattice constants and cosines of angle between the axes. There are [14 possible ibrav numbers](https://pranabdas.github.io/espresso/setup/crystal-structure).
It is also possible to set `ibrav=0` and provide lattice vectors in `CELL_PARAMETERS`, with sufficiently decimal accuracy to facilitate symmetry detection. This is done automatically when creating an input from a CIF file with [cif2cell](cif2cell.md), as
```bash
cif2cell CsPbI3.cif -p quantum-espresso -o relax.in
```

## Structure optimization

Following [Pranabdas' guide](https://pranabdas.github.io/espresso/hands-on/structure-optimization), the relaxation runs with pw.x:
```
pw.x -inp si_relax.in > si_relax.out
```
We should parallelize the code with MPI, from the Slurm file.

## Phonon dispersion

From [Pranabdas' guide](https://pranabdas.github.io/espresso/hands-on/phonon), we have to:
1. Perform SCF calculation using `pw.x`
2. Calculate the dynamical matrix on a uniform mesh of q-points using `ph.x`
3. Perform inverse Fourier transform of the dynamical matrix to obtain inverse Fourier components in real space using `q2r.x`
4. Perform Fourier transformation of the real space components to get the dynamical matrix at any q by using `matdyn.x`
5. Plot the phonon dispersion, etc

HOWEVER, as of [2024](https://www.mail-archive.com/users@lists.quantum-espresso.org/msg44417.html) ph.x does not support the three-body terms with the D3 dispersion correction. Instead, we should use the supercell approach with [Phonopy](https://phonopy.github.io/phonopy/).

## Monkhost-Pack grid

A denser grid leads to a more resolved band structure, however, the computational cost increases significantly. The size of the primitive cell should also be taken into account. For large (super)cells fewer k-points are required since the Brillouin zone is decreased with increasing the cell.

Quantum ESPRESSO also allows for shifting the Monkhost-Pack grid. Depending on the symmetries of the structure, the shift moves the k-point mesh semilattice. The number of inequivalent points then decreases, resulting in a reduction in the total number of k-points.
```shell
K_POINTS (automatic)
Kx Ky Kz 0 0 0 # (non-shifted)
Kx Ky Kz 1 1 1 # (shifted)
```

## Pseudo-potentials

We can choose between Norm-Conserving (NC), PAW and Ultra Soft (US) pseudopotentials.
For MAPI we previously used NC pseudos.
PAW pseudos are better than US for perovskites, according to a [vasp workshop](https://www.vasp.at/vasp-workshop/pseudoppdatabase.pdf).

Quantum ESPRESSO uses pseudos in UPF format, and can be obtained from:
- [Pseudo-Dojo](http://www.pseudo-dojo.org/)
- [Pslibrary](https://dalcorso.github.io/pslibrary/) Need to compile it myself.
- [Standard Solid State PPs (SSSP)](https://www.materialscloud.org/discover/sssp/table/efficiency) "Best verified PPs"
- [Quantum ESPRESSO pseudos](http://pseudopotentials.quantum-espresso.org/)
- [Other PPs resources](https://www.quantum-espresso.org/other-resources/)

## Useful tools
- [cif2cell](cif2cell.md)
- [MaterialsCloud - Quantum ESPRESSO PWscf input generator and structure visualizer](https://www.materialscloud.org/work/tools/qeinputgenerator)
- [MaterialsCloud - Interactive phonon visualizer](https://interactivephonon.materialscloud.io/)
- [MaterialsCloud - See K-path](https://www.materialscloud.org/work/tools/seekpath)
- [YAIV (by Martin) Yet another Ab-Initio Visualizer](https://github.com/mgamigo/YAIV)

## Documentation and tutorials
- [pranabdas' DFT Tutorials using Quantum Espresso](https://pranabdas.github.io/espresso/)
- [Open online course on DFT using Quantum ESPRESSO](https://www.compmatphys.org/)
- [Quantum ESPRESSO input data description](https://www.quantum-espresso.org/documentation/input-data-description/)
- [Quantum ESPRESSO documentation](https://www.quantum-espresso.org/documentation/)

## References
- DFT
- [StackExchange - How to know optimal K-points grid values for good DFT calculation?](https://mattermodeling.stackexchange.com/questions/2347/how-to-know-optimal-k-points-grid-values-for-good-dft-calculation)
- [Quantum Espresso Walkthrough](https://courses.engr.illinois.edu/mse404ela/sp2021/6.DFT-walkthrough.html)
- [Tutorial on IR and Raman spectra with Quantum Espresso](https://blog.larrucea.eu/compute-ir-raman-spectra-qe/)
- [StackExchange - Fixing angles and/or distances in QE](https://mattermodeling.stackexchange.com/questions/7046/how-do-i-relax-only-the-in-plane-component-of-the-unit-cell)

## Troubleshooting

### Error: too many bands are not converged

```
Error in routine c_bands (1):
too many bands are not converged
```

Increase `ecutwfc` and / or decrease `conv_thr`.
([QE users Forum - Too many bands are not converged from nscf calculation](http://www.democritos.it/pipermail/pw_forum/2011-September/022050.html))

Try to decrease `mixing_beta`, or vary other settings from the `&ELECTRONS` block.
([FAQ SCM](https://www.scm.com/doc/QuantumEspresso/faq.html#error-in-routine-c-bands-1-too-many-bands-are-not-converged))

Change the scheme of diagonalization method (at `&ELECTRONS`), e.g. to `diagonalization = ppcg`.
Lower `&ELECTRONS diago_thr_init` to a "reasonable value", such as ~1.0d-7.
([QE users Forum - Too many bands are not converged](https://lists.quantum-espresso.org/pipermail/users/2021-February/046972.html))

### Error: SCF correction compared to forces is large

```
SCF correction compared to forces is large: reduce conv_thr to get better values
```

The code reduces the starting self-consistency threshold `conv_thr` when approaching the minimum energy configuration, up to `conv_thr / upscale`. Reducing `conv_thr` (at `&ELECTRONS`) or increasing `upscale` (at `&IONS`) yields a smoother structural optimization, but if `conv_thr` becomes too small, electronic self-consistency may not converge. You may also increase `etot_conv_thr` and `forc_conv_thr` that determine the threshold for convergence.
([PWscf User's Guide](https://www.quantum-espresso.org/Doc/user_guide_PDF/pw_user_guide.pdf))

It is not an error *per se*, only a warning. If the forces are small it may be usable.
(SOURCE??)

## Error: bfgs failed, convergence not achieved

```
bfgs failed after  85 scf cycles and  79 bfgs steps, convergence not achieved
(criteria: energy <  3.5E-12 Ry, force <  3.9E-07 Ry/Bohr, cell <  1.0E-04 kbar)
```

Make sure that the energy is actually converging. Increasing the number of `electron_maxstep` will only help if the energy is converging slowly. Otherwise if the accuracy is alternating rapidly, or it converges up to a certain value and diverges again, then this might not help at all. That would indicate a problematic input file, or simply that the system may be characterized by ”floppy” low-energy modes, that make very difficult (and of little use anyway) to reach a well converged structure, no matter what.
More relaxed thresholds and a big `upscale` (eg ~1000000)
To check how the SCF accuracy changes, we can use the following command:
```bash
grep -s 'estimated scf accuracy' scf.out 
```
We may then consider reducing `conv_thr` with a less-tightened value.
([Stack Exchange](https://mattermodeling.stackexchange.com/questions/12592/convergence-not-completed-in-scf-for-bands), [PWscf User's Guide](https://www.quantum-espresso.org/Doc/user_guide_PDF/pw_user_guide.pdf))

A desperate option is to copy the final coordinates to the input file and run it again, sometimes it may work. 

