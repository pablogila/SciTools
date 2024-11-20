# ASE

The [Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/index.html) is a set of tools and Python modules for setting up, manipulating, running, visualizing and analyzing atomistic simulations.

## Preparing inputs

We can create structural files for [DFT](https://en.wikipedia.org/wiki/Density_functional_theory) or [Molecular Dynamics](https://en.wikipedia.org/wiki/Molecular_dynamics) software with ASE. We could also create inputs with Materials Studio, but that is paid software.

See example in [[Week 2024-11-04 MDanse#Xray and Neutron Responses]]

For example, we can perform DFT calculations with [CASTEP](CASTEP.md), obtaining CIF structural files. Then, to perform molecular dynamics calculations to these structures, we can use ASE to **transform the CIF files into the PDB format** (Protein DataBase) that [CP2K](https://www.cp2k.org/about) can read.
We can do that with [ase.io](https://wiki.fysik.dtu.dk/ase/ase/io/io.html) as follows:
```python
>>> from ase.io import read
>>> test = read("test.cif")
>>> test.write("test.pdb")
```

## Exporting outputs

We can export outputs from programs such as [Quantum ESPRESSO](Quantum ESPRESSO.md) to a .CIF format.

## Obtaining cell parameters

Sometimes we need the cell parameters: for example, on [[CP2K#CP2K Input|CP2K]] inputs we must specify cell parameters in the `&CELL` section. In order to do that, we can check the cell parameters with the [atoms.cell](https://wiki.fysik.dtu.dk/ase/ase/cell.html) object:
```python
>>> from ase.io import read
>>> test = read("dumped.pdb")
>>> test.cell[:]
array([[35.767,  0.   ,  0.   ],
       [ 0.   , 37.99 ,  0.   ],
       [ 0.   ,  0.   , 33.906]])
```

Optionally, we could just translate the structural file into a `*.cell` file, and copy the `%BLOCK LATTICE_CART` section:
```python
>>> test.write("test.cell")
```
```shell
~$ cat test.cell
%BLOCK LATTICE_CART
35.767000  0.000000  0.000000
 0.000000 37.990000  0.000000
 0.000000  0.000000 33.906000
%ENDBLOCK LATTICE_CART
```

## Visualizing structures

We can check structural files with [VESTA](https://jp-minerals.org/vesta/en/), but we can also visualize them with [ase.visualize.view](https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html) as follows:
```python
>>> from ase.io import read
>>> from ase.visualize import view
>>> test = read("test.pdb")
>>> view(test)
```

## Calculating dipole moments

We can calculate the dipole moment with the `get_dipole_moment()` method, by using another program as a *calculator*. We can use programs such as [CP2K](https://www.cp2k.org/about) as calculators, but seems like CP2K in particular does not support the dipole moment. I checked other programs, but in the end it was a mess and I gave up.

