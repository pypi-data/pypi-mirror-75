# Fslparser 

This package includes fsl parser (FreeSurfer) and vbm parser (NIfTI). 
# How to install
pip install fslvbmparsers
# How to run
import fslvbmparsers \
from fslvbmparsers import parsers \
(X, y) = parsers.fsl_parser(args) \
mask = os.path.join('/computation', mask_directory, mask_file_name) \
(X, y) = parsers.vbm_parser(args, mask)