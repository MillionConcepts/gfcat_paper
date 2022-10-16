import numpy as np
import pyarrow.parquet as pq
import pandas as pd
from lightcurve_interface_skeleton import load_lightcurve_records
import os
from scipy import signal, stats
from rich import print

np.random.seed(19470622) # the birthdate of Bruno Latour

header_data = pd.read_csv('../ref/mislike_image_header_table.csv')

catalog_filename = '../ref/catalog_nd_daostarfinder.parquet'
catalog_file = pq.ParquetFile(catalog_filename)

def find_bright_stars(catalog_file,header_data,n_ecl=100):
    targets=[]
    scrambled_ecl = np.random.choice(len(header_data),size=len(header_data),replace=False)
    #while len(np.unique(np.array(targets)[:,0]))<n_ecl:
    for ix in np.random.choice(len(header_data),size=n_ecl,replace=False):
        visit = header_data.iloc[ix]
        eclipse = int(visit['ECLIPSE'])
        #print(eclipse)
        if visit['EXPTIME']<1500.0:
            continue
        bright_stars = pq.read_table(catalog_filename,filters =
                                     [('aperture_sum_mask_n_51_2','=',0.0),
                                      ('aperture_sum_edge_n_51_2','=',0.0),
                                      ('aperture_sum_n_51_2','>',50000.0),
                                      ('eclipse','=',eclipse)]).to_pandas()

        cps = np.array(bright_stars['aperture_sum_n_51_2'])/visit['EXPTIME']
        ix = np.where(cps>100)
        if not len(cps[ix]):
            #print(f'No bright stars in e{str(eclipse).zfill(5)}')
            continue
        X = list(zip(bright_stars['xcenter'].iloc[ix].tolist(),bright_stars['ycenter'].iloc[ix].tolist()))
        db = DBSCAN(eps=40,min_samples=1).fit(X)
        labels=db.labels_
        for lbl in set(labels):
            dbix = np.where(labels==lbl)[0]
            brightest_ix = np.argmax(cps[ix][dbix])
            star = bright_stars.iloc[ix].iloc[dbix].iloc[brightest_ix]
            cps_12_8,cps_51_2 = (star['aperture_sum_n_12_8']/visit['EXPTIME'],
                                 star['aperture_sum_n_51_2']/visit['EXPTIME'])
            if cps_12_8<=100:
                continue
            # a huge discrepancy between aperture sizes probably means nearby bright stars / field
            if cps_51_2-cps_12_8 > 50:
                continue
            #print(eclipse,int(star['obj_id']),cps_12_8,cps_51_2,cps_51_2-cps_12_8)
            targets+=[[eclipse,int(star['obj_id'])]]
    return targets

targets = find_bright_stars(catalog_file,header_data,n_ecl=1000)
print(len(np.unique(np.array(targets)[:,0])))

def get_lc_summary_stats(lc):
    ad = stats.anderson(lc['cps'])  # standard test of variability
    return {
        'mad':np.mean(np.abs(lc['cps'] - np.mean(lc['cps']))),
        'start_cps':np.median(lc['cps'][:5]),
        'end_cps':np.median(lc['cps'][-6:-1]), # exclude the last bin, which is often low-expt
        'med_std':np.median(lc['cps_err']),
        'ad_statistic':ad.statistic,
        'ad_critical_val':ad.critical_values[2], # 5%
        'xcenter':lc['xcenter'],
        'ycenter':lc['ycenter'],
    }

datadir = '/home/ubuntu/datadir'
for eclipse in np.unique(np.array(targets)[:,0]):
    fn = f'{datadir}/e{str(eclipse).zfill(5)}-30-photom.parquet'
    if os.path.exists(fn):
        continue
    cmd = f'aws s3 cp s3://dream-pool/e{str(eclipse).zfill(5)}/e{str(eclipse).zfill(5)}-30s-photom.parquet {datadir}/.'

for eclipse in np.unique(np.array(targets)[:, 0]):
    fn = f'{datadir}/e{str(eclipse).zfill(5)}-30-photom.parquet'
    aper_radius = 51.2
    lightcurves = load_lightcurve_records(fn, 'NUV', apersize=aper_radius)

    variables = {}
    for lc in lightcurves:
        if lc['obj_id'] in obj_ids:
            variables[lc['obj_id']] = lc
    for obj_id in obj_ids:
        if obj_id not in variables.keys():
            print(f'{obj_id} not found in {eclipse} {band} unflagged lightcurves')

    bright_star_table = pd.DataFrame()
    for k in variables.keys():
        lc = variables[k]
        print(k)
        plt.figure(figsize=(12, 1))
        plt.errorbar(range(len(lc['cps'])), lc['cps'],
                     yerr=lc['cps_err'], fmt='k-')
        plt.xticks([])
        summary_stats = get_lc_summary_stats(lc)
        summary_stats['obj_id'] = int(k)
        summary_stats['eclipse'] = int(str(k)[-5:])
        bright_star_table = bright_star_table.append(pd.Series(summary_stats), ignore_index=True)
bright_star_table = bright_star_table.astype({'obj_id': int, 'eclipse': int})
print(bright_star_table)

bright_star_table.to_csv('brightstar_stats.csv')
