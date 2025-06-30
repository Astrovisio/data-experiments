import numpy as np
import pandas as pd
import os
import sys
from spectral_cube import SpectralCube

def fits_to_dataframe(path):
    # Load the spectral cube
    cube = SpectralCube.read(path)

    df_list = []

    # Iterate over the spectral axis (velocity axis)
    for i in range(cube.shape[0]):
        # Slice one spectral frame at a time
        slab = cube[i, :, :]  # shape: (y, x)

        # Get world coordinates for this frame
        world = slab.wcs.pixel_to_world_values(
            *np.meshgrid(
                np.arange(cube.shape[2]),  # x (RA)
                np.arange(cube.shape[1]),  # y (Dec)
                indexing="xy",
            )
        )

        ra = world[0].flatten()
        dec = world[1].flatten()
        velo = cube.spectral_axis[i].value  # Single velocity value for this slice
        intensity = slab.filled_data[:].value.flatten()
        df_slice = pd.DataFrame(
            {"velocity": velo, "ra": ra, "dec": dec, "intensity": intensity}
        )

        df_list.append(df_slice)

    # Concatenate all slices into a single DataFrame
    df = pd.concat(df_list, ignore_index=True)
    df.dropna(inplace=True)

    del cube

    return df

def check_fits_compatibility(path):
    # Check file existence
    if not os.path.isfile(path):
        print(f"File '{path}' does not exist.")
        return False
    try:
        df = fits_to_dataframe(path)
        df = df[df["intensity"] > 0]  # Remove non-positive intensities
        
        # Check DataFrame is not empty
        if df.empty:
            print("DataFrame is empty after filtering. The file may not have the required data.")
            return False
        # Check all required columns present
        required = ["velocity", "ra", "dec", "intensity"]
        if not all(col in df.columns for col in required):
            print(f"DataFrame does not contain all required columns: {required}")
            return False
        print("The file is compatible.")
        return True
    except Exception as e:
        print(f"Error while loading file: {e}")
        return False

if __name__ == "__main__":
    # Accept file path as a command-line argument or from input
    if len(sys.argv) > 1:
        fits_path = sys.argv[1]
    else:
        fits_path = input("Enter the path to the FITS file: ")
    check_fits_compatibility(fits_path)
