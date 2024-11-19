'''
Script to update the SciTools repository from my Obsidian notes.
Uses InputMaker, https://github.com/pablogila/InputMaker
'''
import inputmaker as im

# Link my Obsidian notes with the final files
dict_files = {
    im.get_file("/home/pablo/Documents/obsidian/Work ⚛️/Instruments/QuantumESPRESSO.md") : "QuantumESPRESSO.md",
    im.get_file("/home/pablo/Documents/obsidian/Work ⚛️/Instruments/CASTEP.md")          : "CASTEP.md",
    im.get_file("/home/pablo/Documents/obsidian/Work ⚛️/Instruments/cif2cell.md")        : "cif2cell.md",
    im.get_file("/home/pablo/Documents/obsidian/Work ⚛️/Instruments/ASE.md")             : "ASE.md",
    im.get_file("/home/pablo/Documents/obsidian/Work ⚛️/Instruments/Zotero.md")          : "Zotero.md",
    im.get_file("/home/pablo/Documents/obsidian/Work ⚛️/Instruments/StructuralDB.md")    : "StructuralDB.md",
    im.get_file("/home/pablo/Documents/obsidian/Work ⚛️/Instruments/Links.md")           : "Links.md",
}

# Dict to fix Obsidian wikilinks
dict_fix = {
    '[[DFT]]'                       : 'DFT',
    '[[Molecular Dynamics]]'        : 'Molecular Dynamics',
    '[[Materials Studio]]'          : 'Materials Studio',
    '[[SLURM]]'                     : 'SLURM',
    '[[Slurm]]'                     : 'Slurm',
    '[[Atlas & Hyperion]]'          : 'Atlas & Hyperion',
    '[[SCARF]]'                     : 'SCARF',
    '[[VESTA]]'                     : '[VESTA](https://jp-minerals.org/vesta/en/)',
    '[[Phonopy]]'                   : '[Phonopy](https://phonopy.github.io/phonopy/)',
    '[[CP2K]]'                      : '[CP2K](https://www.cp2k.org/about)',
    '[[QuantumESPRESSO]]'           : '[QuantumESPRESSO](QuantumESPRESSO.md)',
    '[[CASTEP]]'                    : '[CASTEP](CASTEP.md)',
    '[[cif2cell]]'                  : '[cif2cell](cif2cell.md)',
    '[[ASE]]'                       : '[ASE](ASE.md)',
    '[[ASE#Exporting outputs|ASE]]' : '[ASE](ASE.md)',
    '[[Zotero]]'                    : '[Zotero](Zotero.md)'
}

# Copy and correct Obsidian notes
for original, final in dict_files.items():
    im.copy_to_newfile(original, final)
    im.correct_file_with_dict(final, dict_fix)
# Publish to Git repo
im.git()

