# cif2cell

[cif2cell (GitHub)](https://github.com/torbjornbjorkman/cif2cell) is a tool to generate the geometrical setup for various electronic structure codes from a CIF (Crystallographic Information Framework) file. The code will generate the crystal structure for the primitive cell or the conventional cell.
It can generate [CASTEP](CASTEP.md) CELL input files from CIF files. It is included in the CASTEP academic source bundle.
Since CASTEP is proprietary code, the input files sometimes cause problems when using [ASE](ASE.md) or [VESTA](https://jp-minerals.org/vesta/en/). Also, *cif2cell* works better for creating CELL supercells.

It seems to cause problems in Windows, so you may want to use [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) to run it on that platform. You can download Linux distros such as Ubuntu for WSL from the Microsoft Store.

On Linux, install with:
```bash
pip install cif2cell -U
```

You can use *cif2cell* to create a CELL file from a CIF file.
You can create a supercell in the process with an extra argument, replacing `k,l,m` with the size of the supercell.
Additionally, you can specify the output name with the `-o` tag.
```bash
cif2cell TEST.cif -p castep --supercell=[k,l,m] -o TEST.cell
```

To translate the cell,
```bash
cif2cell TEST.cif -p quantum-espresso --supercell-translation-vector=[k,l,m]
```

