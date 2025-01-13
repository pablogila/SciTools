# CASTEP

## Intro

This is a summary of the [CASTEP (web)](http://www.castep.org/) software for [DFT](https://en.wikipedia.org/wiki/Density_functional_theory) calculations. These notes can be consulted on [GitHub](https://github.com/pablogila/castep4dummies).  
CASTEP developers work in [SCARF](https://www.scarf.rl.ac.uk/index.html), so it is usually updated there.  
To use it in clusters like [Atlas & Hyperion](https://scc.dipc.org/docs/) we have to ask support via email.  

CASTEP has two main ways of calculating the phonon frequencies/modes: **Density-Functional Perturbation Theory (DFPT)** and **Finite-Displacement (FD)**.  
There are different strategies depending on the problem:  
- Primitive cell FD at Γ point  
- Supercell FD for any Q (using traditional, like phonopy, or non-diagonal with Fourier interpolation schemes)  
- DFPT on MP grid of Q with Fourier interpolation to arbitrary fine set of Q  

CASTEP takes advantage of the space-group symmetries of the crystal to compute:  
- ONLY symmetry-independent elements of the dynamical matrix  
- Q-points needed in the 1st Brillouin zone for interpolation  
- Electronic k-points...  

### Useful links

- [CASTEP cell keywords and data blocks](https://www.tcm.phy.cam.ac.uk/castep/documentation/WebHelp/content/modules/castep/keywords/k_main_structure.htm)  
- [The CASTEP Pseudopotential Library](https://www.ccpnc.ac.uk/pspot-site/)  

## General inputs

Keywords that are generally reasonable:  
```castep
grid_scale :              1.75
fine_grid_scale :         4.0
finite_basis_corr :       2
mixing_scheme :           Pulay
mix_charge_amp :          0.500000000000000
mix_charge_gmax :         1.500000000000000
mix_history_length :      20
relativistic_treatment :  Koelling-Harmon
fixed_npw :               false
# To output a cell file with optimized geometry, avoiding copying it from geom:
WRITE_CELL_STRUCTURE :    true
WRITE_CIF_STRUCTURE :     true
```

## Geometry optimization

A high-precision geometry optimization is required. If coordinates are not converged with forces close to zero, phonons will have imaginary frequencies, which are represented in the outputs with negative values.  

The following listed quantities should be converged by systematically variating each one. Values in parenthesis were used by Kacper and Pelayo, and are optimized for perovskites. Other systems may require further job.  

- **Plane wave cutoff.** Usually the larger the better.  
- **SCF convergence.** This is critical in **DFPT**. *elec_energy_tol* should be at least *phonon_energy_tol^2* (`elec_energy_tol : 1e-12` and `phonon_energy_tol : 1e-6` respectively. Also, `max_scf_cycles : 100`).  
- **Brillouin-zone sampling.** Under-convergence results in a poor acoustic mode dispersion as q->0. Use finer grids for **FD** method.  
- **Free energy per atom.** (`1e-10` eV/atom)  
- **Ionic forces.** (`1e-5` eV/A)  
- **Ionic displacement.** (`5e-6` A)  
- **Stress.** (`2.5e-3` GPa)  

Other helpful Keywords:  
```castep
geom_max_iter :  9999
geom_method :    lbfgs
```

## Phonon calculations

### DFPT

DFPT (In the `.param` file)  
```param
task = phonon
phonon_method = dfpt  # Default value
phonon_max_cycles = ...
```

Fourier interpolation:  
```param
phonon_fine_method = interpolate
phonon_kpoint_mp_grid p q r
# ALWAYS INCLUDE Γ
# For EVEN phonon_kpoint_mp_grid parameters:
phonon_fine_kpoint_mp_offset 1/2p 1/2q 1/2r
# To specify Q-path in the .cell file:
phonon_fine_kpoint_path
# To specify the density of Brillouin-zone sampling (alternative to choosing specific set of Q):
kpoints_mp_spacing ...
phonon_force_constant_cutoff  # lower than max-box-dimension/2
```
### FD

FD (in `.param`)  
```param
phonon_method = finite_displacement
phonon_fine_method = interpolation
phonon_kpoint_mp_grid p q r  # CASTEP will produce the supercell, no need to provide it for geometry optimization
phonon_force_constant_cutoff  # < min(p*L1,q*L2,r*L3), where Lx are the lengths of the simulation box specified in .cell
```

FD SUPERCELL (in `.param`):  
```param
phonon_method = finite_displacement
phonon_fine_method : supercell
```

FD SUPERCELL (in `.cell`):  
```cell
supercell_kpoint_list
```

### Helpful keywords

```
calculate_stress :             true
# Population analysis on the final ground state:
popn_calculate :               false
# Check that the acoustic sum rule for phonons is valid:
phonon_sum_rule_method :       reciprocal
phonon_calc_lo_to_splitting :  true
born_charge_sum_rule :         true
phonon_energy_tol :            sqrt(elec_energy_tol of geomopt)
efield_max_cycles :            250
phonon_max_cycles :            100
# Max iterations to compute band-structure:
bs_max_iter :                  250
# During a band structure calculation, number of conjugate gradient steps taken for each electronic band in the electronic minimizer before resetting to the steepest descent direction:
bs_max_cg_steps :              25
bs_eigenvalue_tol :            1.0e-9
```

For room pressure, add to .cell the following:  
```cell
%BLOCK EXTERNAL_PRESSURE
    0.0001013000    0.0000000000    0.0000000000
                    0.0001013000    0.0000000000
                                    0.0001013000
%ENDBLOCK EXTERNAL_PRESSURE
```

**Always** save partial calculations in the `.check` file with the following settings in `.param`:  
```param
num_backup_iter n     (backup every n Q-vectors)
backup_interval t     (backup every t seconds)
```

In the `.cell` file, `SPECIES_LCAO_STATES` refers to the number of subshells preceding the noble gas in the electronic configuration. For example, if the electronic structure of Iodine (I) corresponds to  **(Kr) *4d10 5s2 5p5***  it has value 3, etc. In that case,  
```cell_example
SPECIES_LCAO_STATES :  3
```

## Workflow

### CELL files with cif2cell

CASTEP requires the structures as `.cell` files. To create `.cell` files from `.cif` files we need to use [cif2cell](cif2cell.md) [(see on GitHub)](https://github.com/torbjornbjorkman/cif2cell). We can install it on a given supercluster as follows:  
```shell
# gcc is needed to compile, load it if not ready
module load gcc
# Work in a Python virtual environment (seriously, do it)
python3 -m venv .venv
source ./.venv/bin/activate
# Install cif2cell
pip install cif2cell
```

We can create a supercell in the process of converting the file, adding an extra argument where `k,l,m` is the supercell size. The output name is specified with the `-o` tag.  
```bash
cif2cell TEST.cif -p castep --supercell=[k,l,m] -o TEST.cell
```

To batch convert many `.cell` inputs in one go with *cif2cell*, we can use a script like [InputMaker](https://github.com/pablogila/InputMaker) (deprecated):
```shell
python3 inputmaker.py -castep --supercell=[k,l,m]
```

