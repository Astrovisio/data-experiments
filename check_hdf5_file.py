import pynbody
import pandas as pd
import os
import sys

def pynbody_to_dataframe(path, variables, family=None):
    if family is None:
        sim = pynbody.load(path)
        sim = getattr(sim, str(sim.families()[0]))
    else:
        sim = getattr(pynbody.load(path), family)
    sim.physical_units()
    data = {}
    for var in variables:
        data[var] = sim[var].astype(float)
    df = pd.DataFrame(data)
    del sim
    return df

def check_hdf5_compatibility(path, variables=["x", "y", "z"]):
    # Check file existence
    if not os.path.isfile(path):
        print(f"File '{path}' does not exist.")
        return False
    try:
        df = pynbody_to_dataframe(path, variables)
        # Check DataFrame is not empty
        if df.empty:
            print("DataFrame is empty. The file may not have the required data.")
            return False
        # Check all required columns present
        if not all(var in df.columns for var in variables):
            print(f"DataFrame does not contain all required columns: {variables}")
            return False
        print("The file is compatible.")
        return True
    except Exception as e:
        print(f"Error while loading file: {e}")
        return False

if __name__ == "__main__":
    # Accept file path as a command-line argument or from input
    if len(sys.argv) > 1:
        hdf5_path = sys.argv[1]
    else:
        hdf5_path = input("Enter the path to the HDF5 file: ")
    check_hdf5_compatibility(hdf5_path)
