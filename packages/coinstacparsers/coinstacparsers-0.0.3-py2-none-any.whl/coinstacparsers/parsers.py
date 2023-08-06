#!/usr/bin/env python3


import nibabel as nib
import numpy as np
import os
import pandas as pd

def csv_parser(args):
    """Read the values specified in inputspec.json and return the
    covariate matrix (X) as well the dependent matrix (Y) as dataframes"""
    input_list = args["input"]
    X_info = input_list["covariates"]
    Y_info = input_list["data"]

    X_df = pd.DataFrame.from_dict(X_info).T

    X = X_df.apply(pd.to_numeric, errors='ignore')
    X = pd.get_dummies(X, drop_first=True)
    X = X * 1

    Y_data = Y_info[0]["value"]
    Y_data = pd.DataFrame.from_records(Y_data)
    Y_data.columns = Y_data.iloc[0]
    Y_data = Y_data.drop(Y_data.index[0])

    Y_data.set_index(Y_data.columns[0], inplace = True)
    Y = Y_data.apply(pd.to_numeric, errors = 'ignore')

    ixs = X.index.intersection(Y.index)

    if ixs.empty:
        raise Exception('No common X and Y subjects at ' +args["state"]["clientId"])
    else:
        X = X.loc[ixs]
        Y = Y.loc[ixs]
    Y = Y*1

    return (X, Y)


def parse_for_y(args, y_files, y_labels):
    """Read contents of fsl files into a dataframe"""
    y = pd.DataFrame(index=y_labels)

    for file in y_files:
        if file:
            try:
                y_ = pd.read_csv(
                    os.path.join(args["state"]["baseDirectory"], file),
                    sep='\t',
                    header=None,
                    names=['Measure:volume', file],
                    index_col=0)
                y_ = y_[~y_.index.str.contains("Measure:volume")]
                y_ = y_.apply(pd.to_numeric, errors='ignore')
                y = pd.merge(
                    y, y_, how='left', left_index=True, right_index=True)
            except pd.errors.EmptyDataError:
                continue
            except FileNotFoundError:
                continue

    y = y.T

    return y


def fsl_parser(args):
    """Parse the freesurfer (fsl) specific inputspec.json and return the
    covariate matrix (X) as well the dependent matrix (y) as dataframes"""
    input_list = args["input"]
    X_info = input_list["covariates"]
    y_info = input_list["data"]

    X_df = pd.DataFrame.from_dict(X_info).T

    X = X_df.apply(pd.to_numeric, errors='ignore')
    X = pd.get_dummies(X, drop_first=True)
    X = X * 1

    y_labels = y_info[0]["value"]
    y_files = X.index

    y = parse_for_y(args, y_files, y_labels)

    ixs = X.index.intersection(y.index)

    if ixs.empty:
        raise Exception('No common X and y files at ' +
                        args["state"]["clientId"])
    else:
        X = X.loc[ixs]
        y = y.loc[ixs]

    return (X, y)
	
def nifti_to_data(args, X, mask_file):
    """Read nifti files as matrices"""
    try:
        mask_data = nib.load(mask_file).get_data()
    except FileNotFoundError:
        raise Exception("Missing Mask at " + args["state"]["clientId"])

    appended_data = []

    # Extract Data (after applying mask)
    for image in X.index:
        try:
            image_data = nib.load(
                os.path.join(args["state"]["baseDirectory"],
                             image)).get_data()
            if np.all(np.isnan(image_data)) or np.count_nonzero(
                    image_data) == 0 or image_data.size == 0:
                X.drop(index=image, inplace=True)
                continue
            else:
                appended_data.append(image_data[mask_data > 0])
        except FileNotFoundError:
            X.drop(index=image, inplace=True)
            continue

    y = pd.DataFrame.from_records(appended_data)

    return X, y


def vbm_parser(args, mask):
    """Parse the nifti (.nii) specific inputspec.json and return the
    covariate matrix (X) as well the dependent matrix (y) as dataframes"""
    input_list = args["input"]
    X_info = input_list["covariates"]

    X_df = pd.DataFrame.from_dict(X_info).T

    X = X_df.apply(pd.to_numeric, errors='ignore')
    X = pd.get_dummies(X, drop_first=True)
    X = X * 1

    X.dropna(axis=0, how='any', inplace=True)

    X, y = nifti_to_data(args, X, mask)

    y.columns = ['{}_{}'.format('voxel', str(i)) for i in y.columns]

    return (X, y)


