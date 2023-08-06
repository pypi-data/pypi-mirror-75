#! /usr/bin/env python
# Author: Lilianne Nakazono

import pandas as pd
from paths import *
import numpy as np

def get_known_stars_gal(file, name_class,  verbose=True):
	# This function takes all known stars, galaxies and quasars from file
	# One must give the column name (name_class) where the spectroscopic classes are stored
	#
	if verbose:
		print('Reading table of S-PLUS observations already matched with WISE and SDSS...')

	# Some files may have a # in the beginning of the header
	# Read the first line, if there is a #, drop the # character and save for later
	# Assumptions: .csv is comma delimited file and .txt is whitespace delimited file

	f = open(file)
	line = f.readline()
	f.close()
	line = line.split(',')
	csv = True
	if line[0]=="#":
		line.pop(0)
		if csv:
			alldata = pd.read_table(file, sep=',', comment='#', names = line)
		else:
			alldata = pd.rea_table(file, delim_whitespace=True, comment='#', names = line)
	else:
		if csv:
			alldata = pd.read_table(file, sep=',')
		else:
			alldata = pd.read_table(file, delim_whitespace=True)

	if verbose:
		print('Getting stars from table...')
	STAR_SPLUS = alldata.loc[lambda alldata: alldata[name_class] == 'STAR']
	GAL_SPLUS = alldata.loc[lambda alldata: alldata[name_class] == 'GALAXY']
	QSO_SPLUS = alldata.loc[lambda alldata: alldata[name_class] == 'QSO']

	print('Stars:',len(STAR_SPLUS))
	print('Galaxies:',len(GAL_SPLUS))
	print('QSOs:',len(QSO_SPLUS))


	STAR_SPLUS.index = np.arange(0,len(STAR_SPLUS))
	GAL_SPLUS.index = np.arange(len(STAR_SPLUS), len(GAL_SPLUS)+len(STAR_SPLUS))
	QSO_SPLUS.index = np.arange(len(GAL_SPLUS)+len(STAR_SPLUS),len(GAL_SPLUS)+len(STAR_SPLUS)+len(QSO_SPLUS))

	QSO_SPLUS['target']=0
	STAR_SPLUS['target'] = 1
	GAL_SPLUS['target']=2

	GAL_SPLUS_WISE = GAL_SPLUS[np.isnan(GAL_SPLUS['w1mpro'])==False]
	GAL_SPLUS_WISE = GAL_SPLUS_WISE[np.isnan(GAL_SPLUS_WISE['w2mpro'])==False]
	GAL_SPLUS_WISE = GAL_SPLUS_WISE[np.isnan(GAL_SPLUS_WISE['w1sigmpro'])==False]
	GAL_SPLUS_WISE = GAL_SPLUS_WISE[np.isnan(GAL_SPLUS_WISE['w2sigmpro'])==False]
	GAL_SPLUS_WISE = GAL_SPLUS_WISE[np.isnan(GAL_SPLUS_WISE['w1snr'])==False]
	GAL_SPLUS_WISE = GAL_SPLUS_WISE[np.isnan(GAL_SPLUS_WISE['w2snr'])==False]

	STAR_SPLUS_WISE = STAR_SPLUS[np.isnan(STAR_SPLUS['w1mpro'])==False]
	STAR_SPLUS_WISE = STAR_SPLUS_WISE[np.isnan(STAR_SPLUS_WISE['w2mpro'])==False]
	STAR_SPLUS_WISE = STAR_SPLUS_WISE[np.isnan(STAR_SPLUS_WISE['w1sigmpro'])==False]
	STAR_SPLUS_WISE = STAR_SPLUS_WISE[np.isnan(STAR_SPLUS_WISE['w2sigmpro'])==False]
	STAR_SPLUS_WISE = STAR_SPLUS_WISE[np.isnan(STAR_SPLUS_WISE['w1snr'])==False]
	STAR_SPLUS_WISE = STAR_SPLUS_WISE[np.isnan(STAR_SPLUS_WISE['w2snr'])==False]

	QSO_SPLUS_WISE = QSO_SPLUS[np.isnan(QSO_SPLUS['w1mpro'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['w2mpro'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['w1sigmpro'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['w2sigmpro'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['w1snr'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['w2snr'])==False]

	print('Stars with WISE:',len(STAR_SPLUS_WISE))
	print('Galaxies with WISE:',len(GAL_SPLUS_WISE))
	print('QSOs with WISE:',len(QSO_SPLUS_WISE))

	STAR_NO_WISE = STAR_SPLUS.drop(STAR_SPLUS_WISE.index)
	GAL_NO_WISE = GAL_SPLUS.drop(GAL_SPLUS_WISE.index)
	QSO_NO_WISE = QSO_SPLUS.drop(QSO_SPLUS_WISE.index)

	print('Stars with no WISE:',len(STAR_NO_WISE))
	print('Galaxies with no WISE:',len(GAL_NO_WISE))
	print('QSOs with no WISE:',len(QSO_NO_WISE))

	if verbose:
		print('Converting the columns w1mpro and w2mpro to AB magnitudes...')
	GAL_SPLUS_WISE['w1mpro'] = GAL_SPLUS_WISE['w1mpro'] + 2.699
	GAL_SPLUS_WISE['w2mpro'] = GAL_SPLUS_WISE['w2mpro'] + 3.339
	STAR_SPLUS_WISE['w1mpro'] = STAR_SPLUS_WISE['w1mpro'] + 2.699
	STAR_SPLUS_WISE['w2mpro'] = STAR_SPLUS_WISE['w2mpro'] + 3.339
	QSO_SPLUS_WISE['w1mpro'] = QSO_SPLUS_WISE['w1mpro'] + 2.699
	QSO_SPLUS_WISE['w2mpro'] = QSO_SPLUS_WISE['w2mpro'] + 3.339


	if verbose:
		print('Saving files: ...')
	GAL_SPLUS_WISE.to_csv(spec_path+'/galaxies_WISE_DR16.txt', sep=' ', index=True, index_label='orig_index', na_rep='NaN')
	STAR_SPLUS_WISE.to_csv(spec_path+'/stars_WISE_DR16.txt', sep=' ', index=True,index_label='orig_index', na_rep='NaN')
	QSO_SPLUS_WISE.to_csv(spec_path+'/qso_WISE_DR16.txt', sep=' ', index=True,index_label='orig_index', na_rep='NaN')
	GAL_NO_WISE.to_csv(spec_path+'/galaxies_noWISE_DR16.txt', sep=' ', index=True, index_label='orig_index',na_rep='NaN')
	STAR_NO_WISE.to_csv(spec_path+'/stars_noWISE_DR16.txt', sep=' ', index=True,index_label='orig_index', na_rep='NaN')
	QSO_NO_WISE.to_csv(spec_path+'/qso_noWISE_DR16.txt', sep=' ', index=True,index_label='orig_index', na_rep='NaN')

	files = ['galaxies_WISE_DR16', 'stars_WISE_DR16', 'qso_WISE_DR16',
			 'galaxies_noWISE_DR16', 'stars_noWISE_DR16', 'qso_noWISE_DR16']

	for file in files:
		with open(spec_path+'/'+file+'.txt', "r+") as nfile:
			content = nfile.read()
			nfile.seek(0,0)
			nfile.write("#Created with get_known_stars_gal() from DR1_creating_new_tables.py \n")
			nfile.write("#This does not include objects with missing values for W1 and W2, including signal-to-noises and errors \n")
			nfile.write("#Input file:"+ str(file)+"\n")
			nfile.write("#W1 and W2 are Already converted to AB magnitudes \n")
			nfile.write(content)
		nfile.close()


def get_known_qso(file):

	#This function gets all quasars from DR14Q (previously cross-matched with S-PLUS)
	QSO_SPLUS_WISE = pd.read_table(file,sep=',')
	print(len(QSO_SPLUS_WISE))
	# QSO_SPLUS_WISE.rename(columns={'w1mpro'  :  'w1mpro_2'}, inplace=True)
	# QSO_SPLUS_WISE.rename(columns={'w2mpro'  :  'w2mpro_2'}, inplace=True)
	# QSO_SPLUS_WISE.rename(columns={'w1sigmpro':'w1sigmpro_2'}, inplace=True)
	# QSO_SPLUS_WISE.rename(columns={'w2sigmpro':'w2sigmpro_2'}, inplace=True)
	QSO_SPLUS_WISE.rename(columns={'W1MAG':'w1mpro'}, inplace=True)
	QSO_SPLUS_WISE.rename(columns={'W2MAG':'w2mpro'}, inplace=True)
	QSO_SPLUS_WISE.rename(columns={'ERR_W1MAG':'w1sigmpro'}, inplace=True)
	QSO_SPLUS_WISE.rename(columns={'ERR_W2MAG':'w2sigmpro'}, inplace=True)

	QSO = QSO_SPLUS_WISE

	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['w1mpro'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['w2mpro'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['w1sigmpro'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['w2sigmpro'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['W1SNR'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['W2SNR'])==False]
	QSO_SPLUS_WISE = QSO_SPLUS_WISE[np.isnan(QSO_SPLUS_WISE['Z_2'])==False]
	QSO_SPLUS_WISE['w1mpro'] = QSO_SPLUS_WISE['w1mpro'] + 2.699
	QSO_SPLUS_WISE['w2mpro'] = QSO_SPLUS_WISE['w2mpro'] + 3.339

	QSO_NO_WISE = QSO.drop(QSO_SPLUS_WISE.index)
	QSO_NO_WISE['w1mpro'] = QSO_NO_WISE['w1mpro'] + 2.699
	QSO_NO_WISE['w2mpro'] = QSO_NO_WISE['w2mpro'] + 3.339

	print('QSOs with WISE:',len(QSO_SPLUS_WISE))
	print('QSOs with no WISE:',len(QSO_NO_WISE))

	QSO_NO_WISE.to_csv(spec_path+'/qso_noWISE_DR14Q.txt', sep=' ', index=True, index_label='orig_index', na_rep='NaN')
	QSO_SPLUS_WISE.to_csv(spec_path+'/qso_WISE_DR14Q.txt', sep=' ', index=True,index_label='orig_index', na_rep='NaN')

	files = ['qso_noWISE_DR14Q', 'qso_WISE_DR14Q']
	for file in files:
		with open(spec_path+'/'+file+'.txt', "r+") as nfile:
			content = nfile.read()
			nfile.seek(0,0)
			nfile.write("#Created with get_known_qsol() from DR1_creating_new_tables.py \n")
			nfile.write("#This does not include objects with missing values for W1 and W2, including signal-to-noises and errors \n")
			nfile.write("#Does not include objects with missing value for Z ")
			nfile.write("#Input file:"+ str(file)+"\n")
			nfile.write("#W1 and W2 are Already converted to AB magnitudes \n")
			nfile.write(content)
		nfile.close()

if __name__ == '__main__':

	# file = match_path + '/SPLUS_SQGTool_DR1_complete_v4_specphoto_23'
	# get_known_stars_gal(file, 'class')
	file = match_path + '/SPLUS_DR1_FullStripe82_DR14Q_specphotoDR16.txt'
	get_known_qso(file)

	# file = data_path + '/SPLUS_DR1_FullStripe82_WISE.txt'
	# get_unknowns(file, 'CLASS', 'w1mpro', 'w2mpro')

	# file_qso = table_path + '/Known_QSOs.txt'
	# file_star = table_path + '/Known_stars.txt'
	# match_splus_sdss(file_qso, file)
	# match_splus_sdss(file_star,file)