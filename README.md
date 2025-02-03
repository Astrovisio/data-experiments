# Data Analysis Experiments

This repository contains various experiments in reading, analyzing, and visualizing `.hdf5` or `.ascii` astrophysical files using Python. The experiments are documented in Jupyter notebooks (`.ipynb` files) and cover different aspects of data extraction, transformation, and export.

## Main Findings

1. **Data Loading and Conversion**:
   - `.hdf5` is one of the most commonly used file format for simulation outputs and sharing; it is a hierarchical data format that contains data in a graph that also describes their relationship.
   - `pynbody` looks to be the most promising intermediary between the file and the database, having in it several automatic function to load the most used astrophysical simulation data.
   - A single `.hdf5` file can contain different informations about the same region of space; the most common data that is shared are gas, dark matter, black holes, and stars.


2. **Data Extraction and Transformation**:
   - Some example of simple data transformation that `pynbody` enable include: re-centering data to a new coordinate system, rotating data to align with specific axes, etc...
   - Spatial filtering using masks (e.g., spherical masks) to select regions of interest is possible; the filtered/rotated/centered data can then be exported in a much smaller file.
   - Derived quantities such as mass from density and size are automatically computed by `pynbody` and can be exported as columns in later steps.

3. **Data Export**:
   - Exporting data to different formats such as ASCII and HDF5.
   - The ASCII format, although not standard as a `.csv` would be, is the most used "simple" data format in astrophysics; usually it displays a simple tabular format. I tried to load the exported files using [SPLASH](https://github.com/danieljprice/splash) as well as re-load them into `pynbody` succesfully recreating the exported sphere and visualization.
   - Exporting the same format as a `.hdf5` (meaning in a simple tabular file) is less useful as it is not recognized automatically by pynbody and thus cannot be re-read as easily.
   - As `pynbody` is pretty much `numpy` under the hood, moving the data to `pandas` is a simple operation and allows for easy movement to the db.
   - By choosing only specific variables for export, the size of the simulation can be significantly reduced (from 5GB to as low as 30MB).

## Pipelines

### Extract, Transform, and Export Data

1. **Loading Data**:
   ```python
   import pynbody
   import h5py

   # Load the snapshot
   example_snapshot = pynbody.load(".data/other_data/342447.hdf5")
   example_snapshot.physical_units()
   ```

2. **Extracting Data**:
   ```python
   # Apply a spherical mask to select a region of interest, centered in [0,0,0]
   mask = pynbody.filt.Sphere("70 kpc")
   selected_data = example_snapshot.gas[mask]
   ```

3. **Transforming Data**:
   ```python
   # Re-center the data
   center = pynbody.analysis.halo.center(example_snapshot)
   example_snapshot = center_data(snap=example_snapshot, center_with_units_in=center)

   # Rotate the data
   example_snapshot.rotate_x(-50)
   ```

4. **Exporting Data**:
   ```python
    import numpy as np

    # Export to HDF5
    qt = ["x","y","z","mass","rho"]
    qt_units = [str(s_cut[x].units) for x in qt]

    out_path = ".data/out/gas_illustris_342447_cut"

    with h5py.File(f"{out_path}.hdf5", "w") as f:
        for qt, qt_unit in zip(qt, qt_units):
            xx = np.array(s_cut[qt].in_units(qt_unit))
            __ = f.create_dataset(qt, data = xx)

   # Export to ASCII through pandas
    df = pd.DataFrame([list(s_cut[x].in_units(y)) for x, y in zip(qt, qt_units)]).transpose()
    df.columns = qt

    with open(f"{out_path}.ascii", "w") as f:
        f.write(df.to_string(index=False))
   ```

### Visualization

1. **Density Map**:
   ```python
    map_out = pynbody.plot.sph.image(
                                    f,
                                    width= str(80)+" kpc",
                                    qty="rho",
                                    av_z=None, 
                                    units="Msol kpc^-2",
                                    resolution=512,
                                    cmap="bone",
                                    noplot=False,
                                    )

    plt.show()
   ```


## Notebooks

- test_lettura.ipynb: Demonstrates loading, extracting, and visualizing data from `.hdf5` files.
- test_export.ipynb: Shows how to export data to different formats.
- test_ascii_read.ipynb: Focuses on reading and analyzing ASCII data.
- test_yt.ipynb: Uses the `yt` library for visualization and analysis.
- test_export_2.ipynb: Additional experiments in data extraction and export, a bit more optimized in a phytonic sense compared to test_export.


### To download the illustris_tng dataset (requires login)

https://www.tng-project.org/data/milkyway+andromeda/