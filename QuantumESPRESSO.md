# Quantum ESPRESSO

[Quantum ESPRESSO (web)](https://www.quantum-espresso.org/) is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials modeling at the nanoscale. It is based on [DFT](https://en.wikipedia.org/wiki/Density_functional_theory), [Molecular Dynamics](https://en.wikipedia.org/wiki/Molecular_dynamics), plane waves, and pseudopotentials. It is usually preinstalled in superclusters like [Atlas & Hyperion](https://scc.dipc.org/docs/).

## Input description

These are general indications for the creation of QE inputs. The full list of input parameters is in the [Quantum ESPRESSO input data description](https://www.quantum-espresso.org/documentation/input-data-description/). Inputs can also be created with a graphical interface with [PWgui](http://www-k3.ijs.si/kokalj/pwgui/). Once we know what we are doing this may not be necessary, but until then PWgui is really useful to know what parameters to introduce and so on.

It is useful to follow a custom naming convention for the calculations, as:  
`MATERIAL_yyMMddx_CALCULATION_EXTRA`  
eg.  
`MAPI-ND-5_240729a_relax_test`  

Inputs for *PWsfc pw.x* are a `filename.in`, which is usually called from a Slurm file with MPI paralellization. For example, for a geometry optimization calculation, we would run:
```
mpirun pw.x -inp relax.in > relax.out
```

Input values are in atomic units, unless stated otherwise. This means that energy units are in *Rydbergs*, and distance units in *bohrs*. We can convert between these units easily with the [Maat](https://github.com/pablogila/Maat) python package.

Note that **energy** is an extensive parameter. Consequently, the thresholds for the energy are also extensive, so these depend on the number of atoms of the system.

In general, it is good practice to write exponentials with double precision, with `d` instead of `e`, as in `conv_thr = 1.47d-12`, to avoid weird numeric errors.

**Isotopes** in the [ATOMIC_SPECIES](https://www.quantum-espresso.org/Doc/INPUT_PW.html#ATOMIC_SPECIES) must start by the actual letter from the species, such as H2; It cannot be D.

To export to a .CIF file after the calculation, we can use [ASE](ASE.md). The graphical option would be to open the output on XCrySDen and save it as `.xsf`, then open it on [VESTA](https://jp-minerals.org/vesta/en/) and save it as `.cif`. This last option seems to preserve a bit better the numerical precision, since both [ASE](ASE.md) and [VESTA](https://jp-minerals.org/vesta/en/) cut some decimals for some weird reason. But this can be solved by copying those positions by hand in the final CIF file.

## Crystal structure

In Quantum Espresso, the structure information is provided by `ibrav` number, and corresponding `celldm` values or lattice constants and cosines of angle between the axes. There are only [14 Bravais lattices](https://en.wikipedia.org/wiki/Bravais_lattice#In_3_dimensions), check the [ibrav parameters for QE](https://pranabdas.github.io/espresso/setup/crystal-structure).

It is also possible to set `ibrav=0` and provide lattice vectors in `CELL_PARAMETERS`, with sufficiently decimal accuracy to facilitate symmetry detection. This is done automatically when creating an input from a CIF file with [cif2cell](cif2cell.md), as
```bash
cif2cell CsPbI3.cif -p quantum-espresso -o relax.in
```

To fix the bravais lattice, we must specify the corresponding ibrav number, providing the proper lattice parameters, and adding `cell_dofree='ibrav'`. For example, to fix the lattice at 90º angles, we might want a simple orthorhombic cell, so we set `ibrav=8` and specify A, B and C.
The tag `cell_dofree` specifies which cell parameters should be relaxed, fixing the rest of the cell. Check the [documentation](https://www.quantum-espresso.org/Doc/INPUT_PW.html#idm1160) to see the full list of options.

## Convergence study

For phonons, we will probably need an SCF convergence of `conv_thr=1.0d-10` [or even smaller](https://ashour.dev/Practical+DFT/Iterative+Convergence+Criteria+in+DFT+-+VASP+and+Quantum+ESPRESSO#SCF+convergence+(%60conv_thr%60%2F%60EDIFF%60)).

In most cases, we reach total energy convergence before the forces converge, so the `etot_conv_thr` [is usually not that important](https://ashour.dev/Practical+DFT/Iterative+Convergence+Criteria+in+DFT+-+VASP+and+Quantum+ESPRESSO#Total+Energy+Convergence+(%60etot_conv_thr%60%2F%60EDIFFG%60%3E0)).

For electronic calculations, a `forc_conv_thr` of about $10^{-4}$ Ry/A is commonly found in the literature. Lower values such as $10^{-7}$ Ry/A [may be necessary](https://ashour.dev/Practical+DFT/Iterative+Convergence+Criteria+in+DFT+-+VASP+and+Quantum+ESPRESSO#Force+Convergence+(%60forc_conv_thr%60%2F%60EDIFFG%60%3C0)) for phonon calculations, which is rarely attainable with the usual BFGS algorithm. [Special algorithms](https://iopscience.iop.org/article/10.1088/1361-648X/aacd79) have been developed for such situations.
As a rule of thumb, the forces convergence is roughly the square root of the energy convergence, eg. if energy is converged to $10^{-6}$, forces are converged to ~$10^{-3}$. [(source)](https://mattermodeling.stackexchange.com/questions/13046/negative-phonon-calculation)

The pressure convergence by default is usually okay, but [we might want to reduce](https://ashour.dev/Practical+DFT/Iterative+Convergence+Criteria+in+DFT+-+VASP+and+Quantum+ESPRESSO#Stress%2Fpressure+convergence+(%60press_conv_thr%60%2F%60EDIFFG%3C0%60)) `press_conv_thr` for phonon studies.

**Semiconductors** are commonly treated as insulators, so that `occupations=fixed`. However, if the system is metallic or is difficult to work with numerically, we should apply some [smearing](https://physics.stackexchange.com/questions/360037/what-do-we-physically-mean-by-smearing-in-condensed-matter) to broaden the bands in a continuous spectrum. This would be the case for processes not accounted in the model, such as electron-pnonon interaction, electron-electron scattering, etc.

At the end of every SCF step there is a description of the forces acting on atoms:
```
Forces acting on atoms (cartesian axes, Ry/au):

atom    1 type  1   force =     0.00000620    0.00000000    0.00002841
...
atom    5 type  2   force =    -0.00576159    0.00997884   -0.00407008

Total force =     0.024421     Total SCF correction =     0.000247
```
The `Total force` listed here is the square root of the sum of _all_ of the force components *squared* rather than the sum of the magnitudes of the individual forces on the atoms. This number [is a guide to check overall accuracy](https://eamonnmurray.gitlab.io/modelling_materials/lab05/#forces-in-methane): if the `Total SCF correction` is comparable to the `Total force` it usually means we need to try to better converge the SCF cycle via `conv_thr`.

## Monkhorst-Pack grid

A denser grid leads to a more resolved band structure, however the computational cost increases significantly. The size of the primitive cell should also be taken into account: large (super)cells require fewer k-points, since the Brillouin zone decreases for bigger cells.

Quantum ESPRESSO also allows for shifting the Monkhost-Pack grid. Depending on the symmetries of the structure, the shift moves the k-point mesh semilattice. The number of inequivalent points then decreases, resulting in a reduction in the total number of k-points. However, we should leave it without offset for gamma-point calculations.

```shell
K_POINTS (automatic)
Kx Ky Kz 0 0 0 # (non-shifted)
Kx Ky Kz 1 1 1 # (shifted)
```

See also: [StackExchange - How to know optimal K-points grid values for good DFT calculation?](https://mattermodeling.stackexchange.com/questions/2347/how-to-know-optimal-k-points-grid-values-for-good-dft-calculation)

## Phonon dispersion

From [Pranabdas' guide](https://pranabdas.github.io/espresso/hands-on/phonon), to perform a phonon dispersion we have to:
1. Perform SCF calculation using `pw.x`
2. Calculate the dynamical matrix on a uniform mesh of q-points using `ph.x`
3. Perform inverse Fourier transform of the dynamical matrix to obtain inverse Fourier components in real space using `q2r.x`
4. Perform Fourier transformation of the real space components to get the dynamical matrix at any q by using `matdyn.x`
5. Plot the phonon dispersion, etc

HOWEVER, as of [2024](https://www.mail-archive.com/users@lists.quantum-espresso.org/msg44417.html) ph.x does not support the three-body terms with the D3 dispersion correction. Instead, we should use the supercell approach with [Phonopy](https://phonopy.github.io/phonopy/). This python package is the *de facto* standard for phonon calculations.

## Pseudo-potentials

We can choose between Norm-Conserving (NC), PAW and Ultra Soft (US) pseudopotentials.  
For example, to study perovskites, #druzbicki2024 used NC pseudos, automatically generated by the [CASTEP](CASTEP.md) [DFT](https://en.wikipedia.org/wiki/Density_functional_theory) code.  
PAW pseudos are better than US for perovskites, according to a [vasp workshop](https://www.vasp.at/vasp-workshop/pseudoppdatabase.pdf).  

Quantum ESPRESSO uses pseudos in UPF format, and can be obtained from:
- [Pseudo-Dojo](http://www.pseudo-dojo.org/)
- [Pslibrary](https://dalcorso.github.io/pslibrary/) Need to compile it myself.
- [Standard Solid State PPs (SSSP)](https://www.materialscloud.org/discover/sssp/table/efficiency) "Best verified PPs"
- [Quantum ESPRESSO pseudos](http://pseudopotentials.quantum-espresso.org/)
- [Other PPs resources](https://www.quantum-espresso.org/other-resources/)

## QE documentation
- [Quantum ESPRESSO input data description](https://www.quantum-espresso.org/documentation/input-data-description/)
- [Quantum ESPRESSO documentation](https://www.quantum-espresso.org/documentation/)

## Tutorials
- [MSE404 - Modelling Materials with Density Functional Theory](https://mse404.gitlab.io/labs/) 👍️
- [pranabdas - DFT Tutorials using Quantum Espresso](https://pranabdas.github.io/espresso/) 👍️
- [Open online course on DFT using Quantum ESPRESSO](https://www.compmatphys.org/) 👍️
- [Iterative Convergence Criteria in DFT - VASP and Quantum ESPRESSO](https://ashour.dev/Practical+DFT/Iterative+Convergence+Criteria+in+DFT+-+VASP+and+Quantum+ESPRESSO)
- [Tutorial on IR and Raman spectra with Quantum Espresso](https://blog.larrucea.eu/compute-ir-raman-spectra-qe/)
- [Quantum Espresso Walkthrough](https://courses.engr.illinois.edu/mse404ela/sp2021/6.DFT-walkthrough.html)

## Useful tools
- [cif2cell](cif2cell.md)
- [MaterialsCloud - Quantum ESPRESSO PWscf input generator and structure visualizer](https://qeinputgenerator.materialscloud.io/)
- [MaterialsCloud - Interactive phonon visualizer](https://interactivephonon.materialscloud.io/)
- [MaterialsCloud - See K-path](https://www.materialscloud.org/work/tools/seekpath)
- [YAIV (by Martin) Yet another Ab-Initio Visualizer](https://github.com/mgamigo/YAIV)

## Troubleshooting

### NOTE: The following floating-point exceptions are signalling

```
NOTE: The following floating-point exceptions are signalling: IEEE_UNDERFLOW_FLAG IEEE_DENORMAL
```

Sometimes the slurm output may indicate floating point exceptions as below, which is [irrelevant](https://lists.quantum-espresso.org/pipermail/users/2019-October/043476.html). We can ignore it.

### Error: too many bands are not converged

```
Error in routine c_bands (1):
too many bands are not converged
```

Increase `ecutwfc` and / or decrease `conv_thr`.
([QE users Forum - Too many bands are not converged from nscf calculation](http://www.democritos.it/pipermail/pw_forum/2011-September/022050.html))

Try to decrease `mixing_beta`, or vary other settings from the `&ELECTRONS` block.
([FAQ SCM](https://www.scm.com/doc/QuantumEspresso/faq.html#error-in-routine-c-bands-1-too-many-bands-are-not-converged))

Change the scheme of diagonalization method (at `&ELECTRONS`), e.g. to `diagonalization = ppcg`. Lower `&ELECTRONS diago_thr_init` to a "reasonable value", such as ~1.0d-7. ([QE users Forum - Too many bands are not converged](https://lists.quantum-espresso.org/pipermail/users/2021-February/046972.html))

### Error: SCF correction compared to forces is large

```
SCF correction compared to forces is large: reduce conv_thr to get better values
```

The code reduces the starting self-consistency threshold `conv_thr` when approaching the minimum energy configuration, up to `conv_thr / upscale`. Reducing `conv_thr` (at `&ELECTRONS`) or increasing `upscale` (at `&IONS`) yields a smoother structural optimization, but if `conv_thr` becomes too small, electronic self-consistency may not converge. You may also increase `etot_conv_thr` and `forc_conv_thr` that determine the threshold for convergence. ([PWscf User's Guide](https://www.quantum-espresso.org/Doc/user_guide_PDF/pw_user_guide.pdf))

It is not an error *per se*, only a warning. If the forces are small it may be usable.
(SOURCE?? I forgot the link)

## Error: bfgs failed, convergence not achieved

```
bfgs failed after  85 scf cycles and  79 bfgs steps, convergence not achieved
(criteria: energy <  3.5E-12 Ry, force <  3.9E-07 Ry/Bohr, cell <  1.0E-04 kbar)
```

Make sure that the energy is actually converging. Increasing the number of `electron_maxstep` will only help if the energy is converging slowly. Otherwise if the accuracy is alternating rapidly, or it converges up to a certain value and diverges again, then this might not help at all. That would indicate a problematic input file, or simply that the system may be characterized by ”floppy” low-energy modes, that make very difficult (and of little use anyway) to reach a well converged structure, no matter what. More relaxed thresholds and a big `upscale` could help.

To check how the SCF accuracy changes, we can use the following command:
```bash
grep -s 'estimated scf accuracy' scf.out 
```
We may then consider reducing `conv_thr` with a less-tightened value.
([Stack Exchange](https://mattermodeling.stackexchange.com/questions/12592/convergence-not-completed-in-scf-for-bands), [PWscf User's Guide](https://www.quantum-espresso.org/Doc/user_guide_PDF/pw_user_guide.pdf))

A desperate option is to copy the final coordinates to the input file and run it again, sometimes it may work.

BFGS can rarely hold `forc_con_thr` lower than $10^{-7}$, so making it less tight or even changing the `ion_dynamics` can also work. Damped dynamics takes much longer, but it is more robust. [(source)](https://ashour.dev/Practical+DFT/Iterative+Convergence+Criteria+in+DFT+-+VASP+and+Quantum+ESPRESSO#Force+Convergence+(%60forc_conv_thr%60%2F%60EDIFFG%60%3C0))

 The translational invariance in the calculations is not perfect, which results in a loss of precision in the forces, which can be tricky for low `forc_conv_thr` values. The situation can improve somewhat by increasing the `ecutrho` cutoff. [(source)](https://web.mit.edu/espresso_v6.1/i386_linux26/qe-6.1/PW/Doc/user_guide/node21.html)
 
## Error: dE0s is positive which should never happen

```
Error in routine bfgs (1):
dE0s is positive which should never happen
```

This kind of errors invariably happens when you are very close to the minimum and you have some numerical noise on forces. For most cases, the system is sufficiently  
relaxed.

We can try to run the calculation again. If it persists, slightly modify some atoms randomly and run again. [(source)](https://pw-forum.pwscf.narkive.com/r5X3gkdU/error-in-routine-bfgs-1-de0s-is-positive-which-should-never-happen). You can also try running the calculation from the last positions [(source)](https://pw-forum.pwscf.narkive.com/r5X3gkdU/error-in-routine-bfgs-1-de0s-is-positive-which-should-never-happen).

