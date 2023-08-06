#! /usr/bin/env python
# Author: Lilianne Nakazono

"""
Predict the classification of S-PLUS DR1 using the trained model
from SQGTool_fit.py() and creates a master catalog.
Two classifications are given for each source,
based on the information that is given:
        I. 12 S-PLUS magnitudes + Morphology
        II. 12 S-PLUS magnitudes + W1, W2 magnitudes + Morphology
"""

import time
import numpy as np
import pandas as pd
import pickle
from paths import *

pd.set_option('display.max_columns', None)

__author__ = "Lilianne Mariko Izuti Nakazono"
__version__ = "0.0.5"
__email__ = "lilianne.nakazono@usp.br"
__status__ = "Development"

def read_catalog(filename):
    cat = pd.read_table(match_path + filename, delim_whitespace=True, engine='python')
    return cat

def get_data_wise(data):
    cat_wise = data[pd.isnull(data['w1mpro']) == False]
    cat_wise = cat_wise[pd.isnull(cat_wise['w2mpro']) == False]
    cat_wise = cat_wise[pd.isnull(cat_wise['w1sigmpro']) == False]
    cat_wise = cat_wise[pd.isnull(cat_wise['w2sigmpro']) == False]
    cat_wise['w1mpro'] = cat_wise['w1mpro'] + 2.699
    cat_wise['w2mpro'] = cat_wise['w2mpro'] + 3.339
    return cat_wise


def predict_model_wise(data, filename=result_path + '/DR1_RF_model_wise', verbose=True):
    feat_wise = ['FWHM_n', 'A', 'B', 'KrRadDet', 'uJAVA_auto', 'F378_auto', 'F395_auto',
                 'F410_auto', 'F430_auto', 'g_auto', 'F515_auto', 'r_auto', 'F660_auto', 'i_auto',
                 'F861_auto', 'z_auto', 'w1mpro', 'w2mpro']
    model_wise = pickle.load(open(filename, 'rb'))
    init_time = time.time()
    y_pred = model_wise.predict(data[feat_wise])
    end_time = time.time()
    if verbose:
        print('Elapsed time to classify all sources with WISE counterpart:', end_time - init_time)

    init_time = time.time()
    prob = model_wise.predict_proba(data[feat_wise])
    end_time = time.time()
    if verbose:
        print('Elapsed time to predict probabilities for all sources with WISE counterpart::', end_time - init_time)

    prob = pd.DataFrame(prob)
    prob['CLASS_improved'] = y_pred
    prob.index = data.index
    prob.rename(columns={0: 'PROB_QSO_improved', 1: 'PROB_STAR_improved', 2: 'PROB_GAL_improved'}, inplace=True)
    return prob


def predict_model(data, filename=result_path + '/DR1_RF_model', verbose=True):
    feat = ['FWHM_n', 'A', 'B', 'KrRadDet', 'uJAVA_auto', 'F378_auto', 'F395_auto',
            'F410_auto', 'F430_auto', 'g_auto', 'F515_auto', 'r_auto', 'F660_auto', 'i_auto',
            'F861_auto', 'z_auto']
    model_wise = pickle.load(open(filename, 'rb'))
    init_time = time.time()
    y_pred = model_wise.predict(data[feat])
    end_time = time.time()
    if verbose:
        print('Elapsed time to classify all sources with WISE counterpart:', end_time - init_time)

    init_time = time.time()
    prob = model_wise.predict_proba(data[feat])
    end_time = time.time()
    if verbose:
        print('Elapsed time to predict probabilities for all sources with WISE counterpart::', end_time - init_time)

    prob = pd.DataFrame(prob)
    prob['CLASS_new'] = y_pred
    prob.index = data.index
    prob.rename(columns={0: 'PROB_QSO_new', 1: 'PROB_STAR_new', 2: 'PROB_GAL_new'}, inplace=True)
    return prob


def create_catalog(filename='/SPLUS_DR1_FullStripe82_WISE_all_2arcs.txt', verbose=True):
    if verbose:
        print("Reading S-PLUS catalog...")
    dr1 = read_catalog(filename)

    if verbose:
        print("Creating subset of sources with WISE counterpart...")
    dr1_wise = get_data_wise(dr1)

    if verbose:
        print("STARTING CLASSIFICATION...")
    probabilities = predict_model(dr1)
    probabilities_wise = predict_model_wise(dr1_wise)

    dr1_master = pd.concat([dr1, probabilities, probabilities_wise], axis=1)
    if verbose:
        print("Saving final catalog...")
    dr1_master.to_csv(result_path + '/SPLUS_SQGTool_DR1_v5.csv', sep=',', na_rep='NaN')


if __name__ == '__main__':
    create_catalog()
