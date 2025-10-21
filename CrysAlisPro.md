# CrysAlisPro

CrysAlisPro is a software to analyse single crystal x-ray diffraction measurements, obtaining the lattice parameters and the symmetry of your sample. It outputs the `*.ins` and `*.hkl` files used by [Olex2](https://www.olexsys.org/olex2/) or Jana to determine the crystal structure.
Among other things, it can also estimate the powder diffractogram from the single crystal data, and create unwarp images of the experiment.
It is free of charge, and can be accessed after registration at the [Rigaku X-Ray forum](https://www.rigakuxrayforum.com/).

## Importing data

To open a XRD measurement, CrysAlis can open `*.run` and `*.par` files. It doesn't matter which file we select. Note that everything is saved automatically, so make sure to make a backup of the data before analysing it.

Usually we already have these files, but if we want to start from scratch from the raw measurement files, or to ignore some specific runs, we can open those by running the CrysAlis terminal command:
```CrysAlis
esperanto createrunlist
```

and selecting the desired `/frames/*.rodhypix` files to load. Note that in this case we would also need to load a `*.par` calibration file with the following command:
```CrysAlis
rd p
```

Sometimes we might find some errors in the data analysis due to missing frames. A quick and dirty option is to duplicate a nearby frame and change its name so that there are no gaps in the run.

On the bottom bar we can play all frames, control the zoom, or activate the information cursor for hkl, intensity, angles, etc.
Note that in XRD, Omega is the lab reference angle for the rotation of the sample, and 2Theta is the angle defined from the center of the monitor to the outside border.

We can extend more options at the bottom right corner, next to RED (which indicates that we are in data reduction mode). There we can activate or deactivate the `CCD/Camera reject overlay`. We can also adjust the beamstop with `Adjust beamstop, Edit beamstop`.

## Indexing

### Peak hunt

First we should perform a peak search. Note that this step might have been performed automatically so we might not need to do it.

Clic on the top left button to open the *Lattice Wizard*, and on `Peak hunting` click the `>` button to select `Peak hunting with user settings`. This can also be opened with the CrysAlis command:
```CrysAlis
ph s
```

There we can select tha range of frames to be used for the peak hunting. To ignore a specific run, we can just set its start and end frame to be the same.
For most cases, we would use `Smart peak hunting`. If the data is not very good, such as for high-pressure data, we can use `3D peak extraction`, which also compares between frames.

Once we have hunted the peaks, we can check the peak table with
```CrysAlis
pt e
```

We should save the peak table to a `*.tabbin` file as a backup before integrating the data, with the command
```CrysAlis
wd t
```

We should also `Refine instrument model`.

### Preliminary lattice parameters

We can also determine the lattice parameters from the Ewald explorer, which is more visual and has additional tools to fit to a high-symmetry unit cell. Skip to that section if you want to do it there.

We can determine the lattice parameters directly from the Lattice wizard. First, click on `Unit cell finding with options`. Hopefully you don't have to deal with twinning samples with more than one crystal, but if you do you can specify it here. After running it, you should see the preliminary parameters in the left side of the window, under the line *Constrained current cell*. Check that these are close to the expected ones.
These parameters can be refined by setting a tolerance of indexation of ~0.05 under the `Reindexation with current cell, Change tolerance of indexation` setting, and then clicking several times the `Reindexation with current cell` until they converge. The smaller the threshold, the less points will remain.

But again, this analysis and more can also be performed visually in the Ewald explorer.

#### Ewald explorer

The [Ewald explorer](https://resources.rigaku.com/hubfs/2024%20Rigaku%20Global%20Site/Resource%20Hub/Knowledge%20Library/Rigaku%20Journals/Volume%2035(1)%20-%20Winter%202019/Rigaku%20Journal%2035-1_41-43.pdf?hsLang=en) is a 3D viewer for diffraction space. It is useful to check and refine the data, and to obtain and refine the lattice parameters. We can open it from the Lattice wizard, by clicking `Ewald explorer - reciprocal space`, or with the command:
```CrysAlis
pt ewald
```

We can modify the GUI settings to view the size of the peaks as a function of the intensity by selecting the `f(I)` checkbox.

On the right, we can select which points to show or hide under the `Selection/Lattice-it` tab. We can manually select spurious points with `ctrl+shift` and move them to a different group to hide them. We can also hide the *Wrong* points that it detected automatically.
To exit selection mode, just click on a different tab.

We can process the lattice parameters just as we mentioned from the Lattice wizard.
Once the wrong points are hidden, go to the `Crystal` tab on the right, and click `LATTICE`.
Here we first select `Auto unit cell finding in shown peaks`.
Next, on the same tab, run `Lattice improvement with tolerance`, with a value of ~0.05. Run this again several times until the lattice parameters are not changing anymore.

After this, we can also fit the data to a highly-symmetric unit cell by going to `LATTICE, Modify lattice type`, and selecting the option with the [most meaningful](https://rigaku.com/products/crystallography/learning/cap-tip007) G6-projection distance.

If we created some twins by mistake, we can also remove them from the Ewald explorer. Go to `Crystal, Component #X, Clear twin component`, and repeat for the rest of the twins.

## Unwarp images

To check that the data is decent and that there are no spurious peaks, it might be useful to unwarp the images. This is worth to be shown in a paper, but it is an optional step when reducing the data. Beware that it will take a long time to process.

A synthetic image of any crystallographic plane can be calculated, most commonly views of planes with integer values such that Bragg diffraction spots are visible.
These plane images are called *unwarp* or *simulated precession images*, and can show a two dimensional plane through reciprocal space with pixels generated from real measured intensities.

To generate unwarp images, go to `Lattice wizard, Unwarping - Precession images`, or use the command:
```CrysAlis
dc unwarp
```

Click on `Next` until you can choose `Generate layers`, and write the numbers `3  0.8` on the layers generator. The `3` specifies the number of planes that you want to calculate. With these setting we would obtain 21 images, which is already pretty decent.
To only produce the first 3 images, you can just set `0  0.8`.

## Profile integration

After indexing the peaks, saving the tabbin backup and finding the preliminary lattice parameters, we perform a profile integration.
We can do it by clicking the `START/STOP` button at the top right corner, and then clicking on `Data reduction with options`. An alternative is to use the command:
```CrysAlis
dc proffit
```

On step 3, click on `Edit special pars`, and type `alt+E` to show the hidden parameters, check `Skip model refinement`.

On step 6, change the output name so that it does not overwrite the previous automatic analysis. Also, click on `Edit formula` to introduce the expected chemical elements. Here you should also introduce the expected formula unit `Z` value, this is, the number of molecules in the unit cell. Finally, under *Finalization options*, set the *Space group determination* to `manual`.

Go with the default options for the rest of the sections. Since we set the finalization options to *manual*, it will popup a window to apply some options:
In the *Centering* tabs, make sure that the column with the lowest values is selected.
In the *Space group* tab, try to select the group with the highest symmetry, but also with a low *R(int)* value.
In the *INS-File* tab, check that the chemical formula is right. The program might have changed the Z value. It might have a reason to do so, so if you are not sure you can go with the default Z value, since it should be possible to change it later from [Olex2](https://www.olexsys.org/olex2/) anyway.

## Refinalize

If the data is not good enough, we might have to refinalize the analysis.

Click on the third button from the top left corner to inspect the data.
On the `Red graphs` tab, set `Source data` to `absscale` and check that all values are close to 1 for all frames. If the variation is too high, it indicates that the sample was not in focus.
We should also check the *R(int)* values. Set `Source data` to `rint` to check the *R(int)* value. High values (greater than ~30) indicate poor data quality for those frames.

If we suspect the data is not good enough, we should refinalize it.
To ignore high *R(int)* frames, click on `Refinalize`. On `Space group and AutoChem`, select `Interactive`. On `Filters and limits` select `Manual`, and click on `Filters`, `Add` and choose the `'rint-frame'` filter. There you can filter frames over e.g. 40 *R(int)*.
We can also change the output filename.
Click Ok and go through the refinement.

## Outputs
Main outputs
- `*.res`
- `*.ins`
- `*.hkl`
- `*.cif_od` Oxford Diffraction, for [Jana](https://jana.fzu.cz/)

