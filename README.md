# ABM Transport Network Bangladesh

This repository contains multiple assignments and projects related to the simulation and analysis of transport networks in Bangladesh. The projects focus on modeling, analyzing, and visualizing transport infrastructure, including roads, bridges, and traffic data, using agent-based modeling (ABM) techniques.

## Repository Structure

The repository is organized into the following main folders:

### 1. `Assignment_1/`
This folder focuses on cleaning and correcting raw infrastructure data for bridges and roads in Bangladesh.

- **Key Files:**
  - `fix_bridges.py`: Processes and corrects bridge data from an Excel file.
  - `fix_roads.py`: Processes and corrects road data.
  - `WBSIM/`: Contains infrastructure-related files, including `_roads.tcv` and `BMMS_overview.xlsx`.

- **Key Contributions:**
  - Corrected and standardized bridge and road data for further analysis.
  - Generated a cleaned overview file (`BMMS_overview.xlsx`) summarizing bridge data.
  - Utilized pandas for data manipulation and filtering.

### 2. `Assignment_2/`
This folder introduces simulation models and data preprocessing for transport networks.

- **Key Subfolders:**
  - `data/`: Contains raw and processed data files.
  - `model/`: Houses simulation models for transport networks.
  - `notebook/`: Includes Jupyter notebooks for data preprocessing and visualization.
  - `report/`: Contains reports and documentation.

- **Key Contributions:**
  - Developed a simulation model using `infrastructure.csv` to represent transport networks.
  - Preprocessed data using Jupyter notebooks like `generate_N1.ipynb` to create input files for simulations.
  - Enhanced understanding of transport network dynamics through simulation.

### 3. `Assignment_3/`
This folder builds on the previous assignments by adding advanced analysis and visualization capabilities.

- **Key Subfolders:**
  - `data/`: Contains input data for simulations.
  - `img/`: Stores images and visualizations generated during analysis.
  - `model/`: Contains updated simulation models.
  - `notebook/`: Includes Jupyter notebooks for generating intersections and visualizing results.

- **Key Contributions:**
  - Analyzed simulation results using `model_output.ipynb`.
  - Generated and visualized transport network intersections.
  - Improved simulation models to include intersection analysis and visualization.

### 4. `Assignment_4/`
This folder focuses on advanced data processing and integrating vulnerability and traffic data into the analysis.

- **Key Subfolders:**
  - `data/`: Contains raw and processed data files.
    - **Raw Data:** Includes flood, traffic, bridge, and road data collected from various sources.
    - **Processed Data:** Includes files such as `processed_road_segments.csv` and `bridge_with_traffic.csv`.
  - `notebook/`: Contains Jupyter notebooks for further analysis.
  - `report/`: Includes reports summarizing the findings.

- **Key Contributions:**
  - Processed raw data into usable formats for advanced analysis.
  - Integrated traffic and vulnerability data for bridges and roads.
  - Provided insights into the criticality and resilience of transport infrastructure.




### Contributors

- Alexander Dietz
- Ryan Tan Yi Wei
- Ludwig Branzk
- Corné Snoeij
- Ariel Goldin