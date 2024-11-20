'''
Script to update the SciTools repository from my Obsidian notes.
Uses InputMaker, https://github.com/pablogila/InputMaker
'''
import inputmaker as im

# Link my Obsidian notes with the final files
dict_files = {
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/SciTools.md'        : 'README.md',
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/QuantumESPRESSO.md' : 'QuantumESPRESSO.md',
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/CASTEP.md'          : 'CASTEP.md',
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/cif2cell.md'        : 'cif2cell.md',
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/ASE.md'             : 'ASE.md',
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/Zotero.md'          : 'Zotero.md',
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/StructuralDB.md'    : 'StructuralDB.md',
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/TorrentTrackers.md' : 'TorrentTrackers.md',
}

# Dict to fix Obsidian wikilinks
dict_fix = {
    '[[DFT]]'                       : '[DFT](https://en.wikipedia.org/wiki/Density_functional_theory)',
    '[[Molecular Dynamics]]'        : '[Molecular Dynamics](https://en.wikipedia.org/wiki/Molecular_dynamics)',
    '[[Materials Studio]]'          : 'Materials Studio',
    '[[SLURM]]'                     : 'SLURM',
    '[[Slurm]]'                     : 'Slurm',
    '[[Atlas & Hyperion]]'          : '[Atlas & Hyperion](https://scc.dipc.org/docs/)',
    '[[SCARF]]'                     : '[SCARF](https://www.scarf.rl.ac.uk/index.html)',
    '[[VESTA]]'                     : '[VESTA](https://jp-minerals.org/vesta/en/)',
    '[[Phonopy]]'                   : '[Phonopy](https://phonopy.github.io/phonopy/)',
    '[[CP2K]]'                      : '[CP2K](https://www.cp2k.org/about)',
    '[[Quantum ESPRESSO]]'          : '[Quantum ESPRESSO](Quantum ESPRESSO.md)',
    '[[QuantumESPRESSO]]'           : '[QuantumESPRESSO](QuantumESPRESSO.md)',
    '[[CASTEP]]'                    : '[CASTEP](CASTEP.md)',
    '[[cif2cell]]'                  : '[cif2cell](cif2cell.md)',
    '[[ASE]]'                       : '[ASE](ASE.md)',
    '[[ASE#Exporting outputs|ASE]]' : '[ASE](ASE.md)',
    '[[Zotero]]'                    : '[Zotero](Zotero.md)',
    '[[Torrent trackers]]'          : '[Torrent trackers](Torrent trackers.md)',
    '[[TorrentTrackers]]'           : '[TorrentTrackers](TorrentTrackers.md)',
    '[[StructuralDB]]'              : '[StructuralDB](StructuralDB.md)',
    r'{{'                           : r'{{{',
    '{%'                            : '{\%',
}

# Copy and correct Obsidian notes
for original, final in dict_files.items():
    im.copy_to_newfile(original, final)
    im.correct_file_with_dict(final, dict_fix)
# Correct Zotero notes
zotero_warning = '(Without the `\` symbol; it is just needed for the stupid GitHub pages to load)  '
im.insert_text_under_keyword(zotero_warning, '{\%', 'Zotero.md')
im.insert_text_under_keyword(zotero_warning, r'{{{', 'Zotero.md')
# Publish to Git repo
im.git()

