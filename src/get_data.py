import os
import pandas as pd
import numpy as np

tbl = pd.read_csv('gfcat_visit_table_crossmatched.csv',index_col=None)
eclipses = np.unique(tbl['eclipse'])

for e in eclipses:
        edir = f"e{str(e).zfill(5)}"
    #if not os.path.exists(f"../data/lightcurves/{edir}/"):
    #    os.makedirs(f"../data/lightcurves/{edir}/")
        cmd = f"aws s3 sync s3://dream-pool/{edir} ../data/lightcurves/{edir}/ --exclude '*fits*' --exclude '*gif*' --exclude '*parquet*' --exclude '*full-photom*'"
        cmd = f"aws s3 sync s3://dream-pool/{edir}/ ../data/lightcurves/{edir}/ --exclude '*csv*' --exclude '*parquet*' --exclude '*30s*' --exclude '*jpg*'"
        os.system(cmd)
