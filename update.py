'''
Script to update the SciTools repository from my Obsidian notes.
Uses ATON, https://github.com/pablogila/ATON
'''
from aton import txt
from aton import call
import time

call.here()
date = time.strftime("%Y-%m-%d", time.localtime())

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
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/Git.md'             : 'Git.md',
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/McStas.md'          : 'McStas.md',
    '/home/pablo/Documents/obsidian/Work ⚛️/Instruments/CrysAlisPro.md'     : 'CrysAlisPro.md',
}

# Dict to fix Obsidian wikilinks
dict_fix = {
    '[[DFT]]'                       : '[DFT](https://en.wikipedia.org/wiki/Density_functional_theory)',
    '[[Molecular Dynamics]]'        : '[Molecular Dynamics](https://en.wikipedia.org/wiki/Molecular_dynamics)',
    '[[Materials Studio]]'          : 'Materials Studio',
    '[[SLURM]]'                     : 'SLURM',
    '[[Slurm]]'                     : 'Slurm',
    '[[Hyperion]]'                  : '[Hyperion](https://scc.dipc.org/docs/)',
    '[[SCARF]]'                     : '[SCARF](https://www.scarf.rl.ac.uk/index.html)',
    '[[VESTA]]'                     : '[VESTA](https://jp-minerals.org/vesta/en/)',
    '[[Phonopy]]'                   : '[Phonopy](https://phonopy.github.io/phonopy/)',
    '[[CP2K]]'                      : '[CP2K](https://www.cp2k.org/about)',
    '[[QuantumESPRESSO]]'           : '[QuantumESPRESSO](QuantumESPRESSO.md)',
    '[[CASTEP]]'                    : '[CASTEP](CASTEP.md)',
    '[[cif2cell]]'                  : '[cif2cell](cif2cell.md)',
    '[[ASE]]'                       : '[ASE](ASE.md)',
    '[[ASE#Exporting outputs|ASE]]' : '[ASE](ASE.md)',
    '[[Zotero]]'                    : '[Zotero](Zotero.md)',
    '[[Torrent trackers]]'          : '[Torrent trackers](Torrent trackers.md)',
    '[[TorrentTrackers]]'           : '[TorrentTrackers](TorrentTrackers.md)',
    '[[StructuralDB]]'              : '[StructuralDB](StructuralDB.md)',
    '[[Git]]'                       : '[Git](Git.md)',
    '[[McStas]]'                    : '[McStas](McStas.md)',
    '[[Vitess]]'                    : '[Vitess](https://vitess.fz-juelich.de/)',
    '[[PHITS]]'                     : '[PHITS](https://phits.jaea.go.jp/)',
    '[[CrysAlisPro]]'               : '[CrysAlisPro](CrysAlisPro.md)',
    '[[#Ewald explorer]]'           : 'Ewald explorer',
    '[[Mantid]]'                    : '[Mantid](https://www.mantidproject.org/)',
    '[[Scipp]]'                     : '[Scipp](https://scipp.github.io/)',
    '[[Jana]]'                      : '[Jana](https://jana.fzu.cz/)',
    '[[Olex2]]'                     : '[Olex2](https://www.olexsys.org/olex2/)',
    '[[Naming conventions#For calculations|naming convention]]' : 'naming convention',
    ' ([[Meet 25-03-07-09.00 McStasScript]])' : '',
}

# Copy and correct Obsidian notes
for original, final in dict_files.items():
    txt.edit.from_template(original, final, dict_fix)
txt.edit.insert_at('README.md', f'\n---\nLast updated on {date}',  -1)
# Correct Zotero notes
txt.edit.replace('Zotero.md', '`{%', '`{% raw %}{%')
txt.edit.replace('Zotero.md', '%1}`', '%1}{% endraw %}`')
txt.edit.replace('Zotero.md', '`{{', '`{% raw %}{{')
txt.edit.replace('Zotero.md', '}}`', '}}{% endraw %}`')

call.git()

