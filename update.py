import inputmaker as im

espresso = "/home/pablo/Documents/obsidian/Work ⚛️/Instruments/QuantumESPRESSO.md"
castep   = "/home/pablo/Documents/obsidian/Work ⚛️/Instruments/CASTEP.md"
cif2cell = "/home/pablo/Documents/obsidian/Work ⚛️/Instruments/cif2cell.md"
ase      = "/home/pablo/Documents/obsidian/Work ⚛️/Instruments/ASE.md"
zotero   = "/home/pablo/Documents/obsidian/Work ⚛️/Instruments/Zotero.md"
struct   = "/home/pablo/Documents/obsidian/Work ⚛️/Instruments/StructuralDB.md"

readme_espresso = "QuantumESPRESSO.md"
readme_castep   = "CASTEP.md"
readme_cif2cell = "cif2cell.md"
readme_ase      = "ASE.md"
readme_zotero   = "Zotero.md"
readme_struct   = "StructuralDB.md"

file_espresso = im.get_file(espresso)
file_castep   = im.get_file(castep)
file_cif2cell = im.get_file(cif2cell)
file_ase      = im.get_file(ase)
file_zotero   = im.get_file(zotero)
file_struct   = im.get_file(struct)

dict_files = {
    file_espresso : readme_espresso,
    file_castep   : readme_castep,
    file_cif2cell : readme_cif2cell,
    file_ase      : readme_ase,
    file_zotero   : readme_zotero,
    file_struct   : readme_struct,
}

dict_fix = {
    '[[DFT]]'                : 'DFT',
    '[[Molecular Dynamics]]' : 'Molecular Dynamics',
    '[[Materials Studio]]'   : 'Materials Studio',
    '[[SLURM]]'              : 'SLURM',
    '[[Slurm]]'              : 'Slurm',
    '[[Atlas & Hyperion]]'   : 'Atlas & Hyperion',
    '[[SCARF]]'              : 'SCARF',
    '[[VESTA]]'              : '[VESTA](https://jp-minerals.org/vesta/en/)',
    '[[Phonopy]]'            : '[Phonopy](https://phonopy.github.io/phonopy/)',
    '[[CP2K]]'               : '[CP2K](https://www.cp2k.org/about)',
    '[[QuantumESPRESSO]]'    : '[QuantumESPRESSO](QuantumESPRESSO.md)',
    '[[CASTEP]]'             : '[CASTEP](CASTEP.md)',
    '[[cif2cell]]'           : '[cif2cell](cif2cell.md)',
    '[[ASE]]'                : '[ASE](ASE.md)',
}

# Check if there are differences between original and final files
is_different = False
for original, final in dict_files.items():
    im.copy_to_newfile(original, final)
    im.correct_file_with_dict(final, dict_fix)

im.git()

