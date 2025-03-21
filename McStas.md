# McStas

## Overview

[McStas (web)](https://www.mcstas.org/) is a general tool for **simulating neutron scattering instruments**. It is based on a compiler that reads a high-level specification language defining the instrument to be simulated and produces C code that performs the Monte Carlo Simulation. This makes it very fast, typical figures are 500000 neutron histories per second on a fast PC.

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

## Components

McStas comes with a comprehensive library of well-tested components that include most standard elements of neutron scattering instruments. New components are constantly created by the community.
- [McStas components documentation](https://www2.mcstas.org/download/components/)
- [Shared useful files for McStas](https://www.mcstas.org/download/share/) used to simulate ISIS or ESS instruments

## Workflow

The ESS workflow using McStas is presented in the [ESS DMSM Summer School](https://ess-dmsc-dram.github.io/dmsc-school/intro.html).
Neutron sources can be imported as MCPL files from other MC codes, such as [PHITS](https://phits.jaea.go.jp/).
Then we can use the McStasScript Python API to create the instruments easily.
- [McStasScript](https://mads-bertelsen.github.io/) Python API to make things easier
- [MCPL](https://mctools.github.io/mcpl/) file format to transfer data between different Monte Carlo applications

## Tutorials
- [ESS DMSM Summer School](https://ess-dmsc-dram.github.io/dmsc-school/intro.html). Great tutorial with the ESS workflow, from McStas calculations to data analysis with Scipp
- [McStas and McXtrace schools](https://github.com/McStasMcXtrace/Schools). Repo with learning material from past schools
- [McStasScript-notebooks](https://github.com/PaNOSC-ViNYL/McStasScript-notebooks). Tutorial with McStasScript quizzes
- [Neutron scattering and McStas learning exercises](https://e-learning.pan-training.eu/wiki/Main_Page). Following Kim Leffman's notes

