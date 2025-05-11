# Assignment 1
Goal of the provided scripts is to run a first general clean up process of the Bangladeshi transport network to ensure a high data quality for further assignments.

## Requirements

The provided scripts require Python, preferably Python3 and furthermore, need the Python library. If not already installed, it can be installed with a package manager, like Pip by running:

```bash
pip install pandas
```
Moreover, one needs to have the raw road data folder RMMS, raw bridge data folder BMMS, and the java simulation folder WBSIM in the Assignment_1 folder.
The folder structure should look like this:
 - Assignment_1
	 - BMMS
	 - RMMS
	 - WBSIM
	 - fix_bridges.py
	 - fix_roads.py
	 
## Usage
To run the scripts on can run the following commands in a command line on the "Assignment_1" folder level:

 1. Clean Road Data
To clean the road data, one should run the fix_roads.py file. This script creates a _roads3.csv file used for cleaning the bridge data, and a _roads.tcv used for the road visualization.
```bash
python3 fix_roads.py
```
 2. Clean Bridge Data
 To clean the bridge data, one should run the fix_bridges.py file. This script creates BMMS_overview.xlsx for the bridge visualization.
 ```bash
python3 fix_bridges.py
```


