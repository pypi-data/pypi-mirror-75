# coinstacparsers 

This package includes fsl_parser, vbm_parser and csv parser. fsl_parser parses the freesurfer files (specified in inputspec.json) as dependencies and returns 
the covariates (X) and dependent (y) matrices as dataframes. The format of inputspec.json should be as shown in the example inputspec.json here.
Similarly vbm_parser parses NIfTI images as dependencies and returns the covariates (X) and dependent (y) matrices as dataframes. 
csv_parser reads the values specified in inputspec.json file and returns the covariates (X) and dependent (y) matrices as dataframes.
# How to install
pip install coinstacparsers
# How to run
for fsl parser: \
 &nbsp;&nbsp;&nbsp;&nbsp; import coinstacparsers \
 &nbsp;&nbsp;&nbsp;&nbsp; from coinstacparsers import parsers \
 &nbsp;&nbsp;&nbsp;&nbsp; args = json.loads(sys.stdin.read()) \
 &nbsp;&nbsp;&nbsp;&nbsp; (X, y) = parsers.fsl_parser(args) \
for vbm parser: \
 &nbsp;&nbsp;&nbsp;&nbsp; import coinstacparsers \
 &nbsp;&nbsp;&nbsp;&nbsp; from coinstacparsers import parsers \
 &nbsp;&nbsp;&nbsp;&nbsp; args = json.loads(sys.stdin.read()) \
 &nbsp;&nbsp;&nbsp;&nbsp; mask = os.path.join('/computation', mask_directory, mask_file_name) \
 &nbsp;&nbsp;&nbsp;&nbsp; (X, y) = parsers.vbm_parser(args, mask)
for csv parser: \
 &nbsp;&nbsp;&nbsp;&nbsp; import coinstacparsers \
 &nbsp;&nbsp;&nbsp;&nbsp; from coinstacparsers import parsers \
 &nbsp;&nbsp;&nbsp;&nbsp; args = json.loads(sys.stdin.read()) \
 &nbsp;&nbsp;&nbsp;&nbsp; (X, y) = parsers.csv_parser(args)
 