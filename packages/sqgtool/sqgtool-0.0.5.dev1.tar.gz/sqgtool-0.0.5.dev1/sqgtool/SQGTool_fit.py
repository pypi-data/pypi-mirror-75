#! /usr/bin/env python

"""
Fit a supervised Random Forest algorithm
    Classes: star, quasar and galaxy
    Training set: SDSS spectroscopic sample
    Feature spaces:
        I. 12 S-PLUS magnitudes + Morphology
        II. 12 S-PLUS magnitudes + W1, W2 magnitudes + Morphology
"""

import time
from tqdm import tqdm
import numpy as np
import pandas as pd
import pickle
from astropy.stats import sigma_clip, mad_std
from sklearn.ensemble import RandomForestClassifier
from paths import *
from sqgtool.DR1_creating_new_tables import get_known_stars_gal, get_known_qso

__author__ = "Lilianne Mariko Izuti Nakazono"
__version__ = "0.0.5"
__email__ = "lilianne.nakazono@usp.br"
__status__ = "Development"


class ClassifierFull:
    package = 'sklearn'
    algorithm = 'RandomForestClassifier'
    version = __version__

    def __init__(self, save_path=None, verbose=True):
        self.verbose = verbose
        self.qso, self.qso_wise, self.star_wise, self.star, self.gal_wise, self.gal = self.read_data()
        self.qso.name = "qso"
        self.qso_wise.name = "qso_wise"
        self.star.name = "star"
        self.star_wise.name = "star_wise"
        self.gal.name = "gal"
        self.gal_wise.name = "gal_wise"
        self.clf_I, self.clf_II = self.train_classifier()

        if save_path:
            pickle.dump(self.clf_I, open(save_path, 'wb'))
            pickle.dump(self.clf_II,
                        open(save_path + '_wise', 'wb'))

    def read_data(self):
        if not (os.path.exists(spec_path + '/stars_WISE_DR16.txt') or
                os.path.exists(spec_path + '/stars_noWISE_DR16.txt') or
                os.path.exists(spec_path + '/galaxies_WISE_DR16.txt') or
                os.path.exists(spec_path + '/galaxies_noWISE_DR16.txt')):
            get_known_stars_gal(match_path + '/SPLUS_SQGTool_DR1_complete_v4_specphoto_23', 'class')
            if self.verbose:
                print("Created stars and galaxies files into " + spec_path + " folder.")

        if not (os.path.exists(spec_path + '/qso_noWISE_DR14Q.txt') or
                os.path.exists(spec_path + '/qso_WISE_DR14Q.txt')):
            get_known_qso(match_path + '/SPLUS_DR1_FullStripe82_DR14Q_specphotoDR16.txt')
            if self.ve  rbose:
                print("Created quasars files into " + spec_path + " folder.")

        if self.verbose:
            print("Reading spectroscopic data files...")
        qso = pd.read_table(spec_path + '/qso_noWISE_DR14Q.txt',
                            delim_whitespace=True, comment='#', header=0)
        qso_wise = pd.read_table(
            spec_path + '/qso_WISE_DR14Q.txt', delim_whitespace=True, comment='#', header=0)
        star_wise = pd.read_table(
            spec_path + '/stars_WISE_DR16.txt', delim_whitespace=True, comment='#', header=0)
        star = pd.read_table(spec_path + '/stars_noWISE_DR16.txt',
                             delim_whitespace=True, comment='#', header=0)
        gal_wise = pd.read_table(spec_path + '/galaxies_WISE_DR16.txt',
                                 delim_whitespace=True, comment='#', header=0)
        gal = pd.read_table(spec_path + '/galaxies_noWISE_DR16.txt',
                            delim_whitespace=True, comment='#', header=0)

        if self.verbose:
            print("Completed reading files.")

        return qso, qso_wise, star_wise, star, gal_wise, gal

    def add_target_col(self):
        for data in [self.qso, self.qso_wise, self.star_wise, self.star, self.gal_wise, self.gal]:
            if "qso" in data.name:
                data['target'] = 0
            elif "star" in data.name:
                data['target'] = 1
            else:
                data['target'] = 2

    def get_train_set(self):

        if self.verbose:
            print("Adding column 'target' for each sample where:")
            print("0 - QSO; 1 - STAR ; 2 - GALAXY")

        self.add_target_col()

        if self.verbose:
            print("Creating the training sets...")

        train_set_wise = pd.concat([self.qso_wise, self.star_wise, self.gal_wise], axis=0, sort=False,
                                   ignore_index=True)
        train_set = pd.concat([train_set_wise, self.qso, self.star, self.gal], axis=0, sort=False, ignore_index=True)

        return train_set_wise, train_set

    def train_classifier(self):
        train_set_wise, train_set = self.get_train_set()
        feat_wise = ['FWHM_n', 'A', 'B', 'KrRadDet', 'uJAVA_auto', 'F378_auto', 'F395_auto',
                     'F410_auto', 'F430_auto', 'g_auto', 'F515_auto', 'r_auto', 'F660_auto', 'i_auto',
                     'F861_auto', 'z_auto', 'w1mpro', 'w2mpro']
        feat = ['FWHM_n', 'A', 'B', 'KrRadDet', 'uJAVA_auto', 'F378_auto', 'F395_auto',
                'F410_auto', 'F430_auto', 'g_auto', 'F515_auto', 'r_auto', 'F660_auto', 'i_auto',
                'F861_auto', 'z_auto']

        clf_wise = RandomForestClassifier(random_state=2, n_estimators=100, bootstrap=True)
        if self.verbose:
            print("Fitting classifier with WISE:")
            print(clf_wise)
            print("With following features: ", feat_wise)
        init_time = time.time()
        clf_wise.fit(train_set_wise[feat_wise], train_set_wise['target'])
        end_time = time.time()
        if self.verbose:
            print("Elapsed time for training the classifier: {:.2f}".format(end_time - init_time), 'seconds.')

        clf = RandomForestClassifier(random_state=2, n_estimators=100, bootstrap=True)
        if self.verbose:
            print("Fitting classifier without WISE:")
            print(clf)
            print("With following features: ", feat)
        init_time = time.time()
        clf.fit(train_set[feat], train_set['target'])
        end_time = time.time()
        if self.verbose:
            print("Elapsed time for training the classifier: {:.2f}".format(end_time - init_time), 'seconds.')

        return clf_wise, clf


class ClassifierCleaned(ClassifierFull):  # inherits ClassifierFull methods
    @staticmethod
    def sigma_clip(data, mag_splus='r_auto', mag_sdss='modelmag_r_2', sigma_value=4):
        """
        Performs n-sigma clipping per magnitude bin (size 0.5)
        Objects with missing values in any of mag_splus or mag_sdss bands are maintained

        Parameters
        ----------
        data:
            Dataframe containing mag_splus and mag_sdss columns
        mag_splus: str
            name of the column for  S-PLUS magnitude
        mag_sdss: str
            name of the columns for the SDSS magnitude (similar band and same aperture as mag_splus)
        sigma_value:
            defines how many sigma away from the mean will be our threshold

        Returns
        -------
        final_data:
            Dataframe cleaned by sigma-clipping
        """

        min_value = np.floor(np.min(data.query(mag_splus + '!=99 and ' + mag_splus + '!=-99')[mag_splus]))
        max_value = np.ceil(np.max(data.query(mag_splus + '!=99 and ' + mag_splus + '!=-99')[mag_splus]))


        idx_rejected = []
        for i in np.arange(min_value, max_value, 0.5):
            mask = (data[mag_splus] > i) & (data[mag_splus] <= i + 0.5) #set magnitude range
            filtered_data = sigma_clip(
                data[mask][mag_sdss] - data[mask][mag_splus], sigma=sigma_value, maxiters=5, stdfunc=mad_std, return_bounds=True)
            if len(filtered_data) != 0: #check if there are objects being rejected in a specific magnitude range
                mask_rejected = filtered_data[0].mask
                idx_rejected = idx_rejected + data[mask][mask_rejected].index.get_level_values(0).values.tolist() #stores the true index of the rows rejected by sigma clipping
        data.drop(idx_rejected, inplace=True) # updates data without rejected objects)
        return data

    def filter_data(self):
        """
        Updates data by cleaning spurious sources depending of the class
        Criteria for maintaining objects are:
            - QSO: PhotoFlag == 0
            - STAR: PhotoFlag == 0 & r_auto > 13
            - GAL: PhotoFlag == 0 & zWarning == 0
        Apply sigma_clip() to each sample
        """

        cond_qso = "PhotoFlag==0"
        cond_star = "PhotoFlag == 0 and r_auto>13"
        cond_gal = "PhotoFlag == 0 and zWarning_2 == 0"

        for df in tqdm([self.qso, self.qso_wise, self.star, self.star_wise, self.gal, self.gal_wise]):
            if "qso" in df.name:
                df.query(cond_qso, inplace=True)
            elif "star" in df.name:
                df.query(cond_star, inplace=True)
            else:
                df.query(cond_gal, inplace=True)
            self.sigma_clip(df)

    def get_train_set(self):
        if self.verbose:
            print('Original size:')
            for df in [self.qso, self.qso_wise, self.star_wise, self.star, self.gal_wise, self.gal]:
                df.index.name = "idx"
                print('      ', df.name, '->', len(df))
            print("Adding column 'target' for each sample where:")
            print("0 - QSO; 1 - STAR ; 2 - GALAXY")
            print("Cleaning spectroscopic data...")

        self.add_target_col()
        self.filter_data()  # filter spurious sources

        if self.verbose:
            print('Cleaned size:')
            for df in [self.qso, self.qso_wise, self.star_wise, self.star, self.gal_wise, self.gal]:
                print('      ', df.name, '->', len(df))

            print("Creating the training sets...")

        train_set_wise = pd.concat([self.qso_wise, self.star_wise, self.gal_wise], axis=0, sort=False,
                                   ignore_index=True)
        train_set = pd.concat([train_set_wise, self.qso, self.star, self.gal], axis=0, sort=False, ignore_index=True)
        return train_set_wise, train_set


if __name__ == '__main__':
    save_filename = result_path + '/DR1_RF_model'
    model = ClassifierCleaned(save_path=save_filename, verbose=True)
