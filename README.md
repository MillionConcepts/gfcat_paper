# GFCAT (paper)

This is the working repository for the summary paper for the GALEX Flare Catalog (GFCAT) project to mine the GALEX archival data corpus for variables serendipitously observed at timescales less than about 30 minutes. The reference repository for this project is at [https://github.com/millionconcepts/gfcat](https://github.com/millionconcepts/gfcat)

The contents of this repository were in support of a large research project spread over many years. They are similar in kind to unedited lab notebooks and should be approached with that attitude. A summary publication is in preparation. Prior to that, **if you use the contents of this repository in your research, cite the gfcat repository with its Zenodo identifier**: `Million, Chase, Scott W. Fleming, "GFCat" https://github.com/MillionConcepts/gfcat (2020). DOI:10.5281/zenodo.4147590.`

The software required for compiling the final figures and results for the paper are contained in a series of Jupyter Notebooks in the `src` directory with names that start with a three digit number "00N -". These should be executed in order. However, they may refer to data files (e.g. FITS movie and image data, or other reference files) that are _not_ included in this repository (because it is many terabytes in total data volume and can be reproduced with gPhoton2). The notebooks import support software also contained in the repository as well as other dependencies obtainable via `conda`.

A full copy of the intermediate data is being retained by the PI in an institutional repository. Final data for GFCAT---comprising light curve files, QA images, and catalog files---is publicly archived at **[LOCATION TBD]**

This work was supported by NASA ADAP Grant 80NSSC18K0084.
