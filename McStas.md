# McStas

## Overview

[McStas (web)](https://www.mcstas.org/), [(Manual)](https://www.mcstas.org/documentation/manual/) is a general tool for **simulating neutron scattering instruments**. It is based on a compiler that reads a high-level specification language defining the instrument to be simulated and produces C code that performs the Monte Carlo Simulation. This makes it very fast, typical figures are 500000 neutron histories per second on a fast PC.

It is common to test calculations in more than one software to check their validity; an alternative to McStas is [Vitess](https://vitess.fz-juelich.de/).

McStas shares codebase with its X-Ray analogous, [McXtrace](https://www.mcxtrace.org/), with a similar syntax.

## Installation

### On PC

It is recommended to [install McStas](https://github.com/mccode-dev/McCode/blob/main/INSTALL-McStas/conda/README.md#if-you-dont-have-a-conda-already) with [miniforge](https://conda-forge.org/download/).
Once miniforge is installed, create a conda environment and install McStas:
```bash
conda create --name mcstas
conda activate mcstas
mamba install mcstas
```

### On HPC clusters

To use McStas in HPC clusters like [Hyperion](https://scc.dipc.org/docs/), it should be installed in the /scratch folder.
Replacing `gila` by your own username,
```bash
module load Python
conda create --prefix /scratch/gila/.conda/envs/mcstas
conda activate /scratch/gila/.conda/envs/mcstas
conda install mamba --channel conda-forge
mamba install mcstas
```

Once installed, it can be accessed anytime as
```bash
module load Python
conda activate /scratch/gila/.conda/envs/mcstas
```

## Components and resources

McStas comes with a comprehensive library of well-tested components that include most standard elements of neutron scattering instruments. New components are constantly created by the community. Neutron sources can also be imported from other programs.
- [McStas components documentation](https://www2.mcstas.org/download/components/)
- [McStas Manual](https://www.mcstas.org/documentation/manual/) has a components manual
- [Shared useful files for McStas](https://www.mcstas.org/download/share/) used to simulate ISIS or ESS instruments
- [MCPL](https://mctools.github.io/mcpl/) file format to transfer data between different Monte Carlo applications, for example to use sources from [PHITS](https://phits.jaea.go.jp/) calculations.
- [McStasToX](https://github.com/mccode-dev/McStasToX/). Package to read McStas data and export to other software, such as [[Scipp]]

## McStasScript

[McStasScript](https://mads-bertelsen.github.io/) is the McStas Python API, really useful to automatize calculations and to make things easier. The ESS workflow using McStas is presented in the [ESS DMSC Summer School](https://ess-dmsc-dram.github.io/dmsc-school/intro.html).

McStasScript provides really useful help commands that can guide you when designing instruments in Jupyter Lab:
```python
import mcstasscript as ms
instrument = ms.McStas_instr("MyInstrument")

instrument.available_components()
# Shows all available component categories

instrument.available_components("sources")
# All available components from a specific category

instrument.component_help("Source_custom")
# Help for a specific component
```

You can also see the parameters of a component that you already placed,
```python
source = instrument.add_component("MySource", "Source_custom")
monitor = instrument.add_component("monitor", "L_monitor")

source.show_parameters()
# Shows current parameters used in the component

source.set_parameters(xwidth=0.1, ...)
```

You should configure the instrument settings before running the simulation:
```python
instrument.settings(ncount=1e7, mpi=4, ...)
instrument.show_settings()
# Shows current instrument settings
```

Finally, run the simulation and plot the data from the monitors that you placed on the instrument:
```python
data = instrument.backengine()
ms.make_plot(data)
```

The handy functions `ms.make_plot()` and `ms.make_sub_plot()` have *some* [customization options](https://mads-bertelsen.github.io/user_guide/plotting.html), but if you want more control you can just plot the data with [Matplotlib](https://matplotlib.org/cheatsheets/)
```python
measurement_L = ms.name_search("L_monitor", data)
wavelength = measurement_L.xaxis
intensity = measurement_L.Intensity
plt.plot(wavelength, intensity)
plt.show()
```

## Export to NeXus files

In the future, there will be tools to import McStas data to [[Scipp]], such as [McStasToX](https://github.com/mccode-dev/McStasToX/). We can, however, export the results to a [NeXus](https://manual.nexusformat.org/introduction.html) [HDF5](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) file, which is compatible with both [[Mantid]] and Scipp. To do so, some additional considerations are required:
- Run the simulation with the `NeXus=True` flag, and `custom_flags='--IDF'`
- The instrument name should follow `*_Mantid`
- Include the dependency `" @NEXUSFLAGS@ "`
- The source (or arm at source position) must be named `sourceMantid`
- The sample must be named `sampleMantid`
- Event monitors Monitor_nD must be named `nD_Mantid_#`
- The Monitor_nD options for a square 16x16 monitor should be similar to `"mantid square x limits=[-0.08 0.08] bins=100 y limits=[-0.08 0.08] bins=100, neutron pixel min=0 t, list all neutrons"`. Note that since Mantid requires pixels to have an unique ID, a second monitor should have a higher `min` value (>bins²) to avoid overlapping IDs.

An example to export a very simple diffractometer to [[Mantid]]:
```python
# Definitions of custom distances and sizes, in meters
dist_src_sam = 4
dist_sam_mon = 0.30
xw_mon = 0.15
yh_mon = 0.15

# Special parameters to export a NeXus file
instrument = ms.McStas_instr(
	'MyInstrument_Mantid'
	...
	NeXus = True,
	custom_flags = '--IDF'
	)
instrument.set_dependency(" @NEXUSFLAGS@ ")

# Instrument components etc
source = instrument.add_component("sourceMantid", "Source_custom", AT=[0,0,0])
sample = instrument.add_component("sampleMantid", "PowderN", AT=dist_src_sam)
# Monitors can be situated from a virtual arm for easy positioning
arm = instrument.add_component("arm", "Arm", AT=[0,0,0], RELATIVE=sample, ROTATED=[-90,0,0])
monitor = instrument.add_component("nD_Mantid_1", "Monitor_nD", AT=dist_sam_mon, RELATIVE=arm)

# Set the parameters for the Monitor_nD
monitor.set_parameters(
	options ='"mantid square x bins=100 y bins=100, neutron pixel min=0 t, list all neutrons"',
	xwidth = xw_mon,
	yheight = yh_mon,
	restore_neutron = 1,
	)

# Set parameters for the source and sample etc...
```

When using a banana monitor, the xwidth will be the diameter of the full banana. Therefore, a banana monitor should be placed centered at the sample position, with the xwidth being double the distance from the centered sample to the surface of the monitor. The angle is specified with the theta variable.
```python
monitor.set_parameters(
	options ='"mantid banana, theta limits=[-15 15] bins=100, y bins=100, neutron pixel min=0 t, list all neutrons"',
	xwidth = dist_sam_mon*2,
	yheight = yh_mon,
	restore_neutron = 1,
	)
monitor.set_AT([0,0,0], RELATIVE=arm)
```

## Beware of the binning

Since we mostly measure **histograms** of neutron counts per wavelength or energy range, the binning will be very important to properly normalise the data. This implies not only the number of bins, but also the range of wavelengths or energies that we are measuring.
A proper normalisation of the intensities is performed by dividing the intensity by the size of the individual bin. This is the same as multiplying by the number of bins and dividing by the whole measuring range. Additionally, we should also normalise by the detector area, in cm² units. Also, if we want to plot per μA, and our source was e.g. 100 μA, we should consider it as well:
```python
measurement = ms.name_search("L_monitor", data)
I = measurement.Intensity * binning / (Lmax-Lmin) / (xw*100 * yh*100) / 100
```

==THE FOLLOWING IS NOT ACCURATE:==
If we normalise the intensity from a neutron *energy* measurement (E_monitor) by the size of the energy bin, the intensity will be in units of energy. On the other side, If we normalise the intensity of a *wavelength* measurement (L_monitor) by the size of the wavelength bin, and *then* we convert the x axis to energy, it will be in *lethargy* units. Remember the De Broglie conversion from neutron wavelength to energy,
$$E = \frac{h}{2m\lambda^2}$$
$$E[meV] = \frac{81.82}{(\lambda[AA])^2}$$
$$\lambda[AA] = \sqrt{\frac{81.82}{E[meV]}}$$

## Tutorials
- [ESS DMSC Summer School](https://ess-dmsc-dram.github.io/dmsc-school/intro.html). Great tutorial with the ESS workflow, from McStas calculations to data analysis with Scipp
- [McStas and McXtrace schools](https://github.com/McStasMcXtrace/Schools). Repo with learning material from past schools
- [McStasScript-notebooks](https://github.com/PaNOSC-ViNYL/McStasScript-notebooks). Tutorial with McStasScript quizzes
- [Neutron scattering and McStas learning exercises](https://e-learning.pan-training.eu/wiki/Main_Page). Following Kim Leffman's notes
- [McStas and Mantid integration](https://github.com/mccode-dev/McCode/wiki/McStas-and-Mantid) GitHub Wiki

