# Simulation of Transport Networks in Bangladesh

Created by: EPA1352 Group 09 

| Name    | Student Number |
|:-------:|:--------|
| Alexander Dietz  | 5859549 | 
| Ryan Tan Yi Wei | 5708427 |
| Ludwig Branzk | 5862515 |
| Corné Snoeij | 5174473 |
| Ariel Goldin | 5354717 |


## Introduction

This simulation model is based on the simple transport model demo, see [./model/model.py](./model/model.py) for EPA1352 Advanced Simulation course Assignment 2. The model is based on the MESA framework.
The current implementation foucses on the most important roads of Bangladesh, N1, N2 and all connected N-Roads that are longer than 25km. Goal of this model is to simulate scenarios in which bridges break down and how these events affect the individual travel time due to delay. Moreover, we can also assess
wich bridges are most important for the overall travel time and hence, should be the focus of maintenance.

## How to Use

To use the simulation, one needs to have all packages installed that are listed in the requirements.txt file. To install all packages with pip, run the following command in the terminal:

``` 
pip install -r requirements.txt
```

There are two modes to run the simulation. The first one is to run the simulation with visualization. This mode is useful to get a better understanding of the model and the simulation. The second mode is to run the simulation without visualization. This mode is useful to run the simulation for a longer time and to collect data for further analysis. We recommend to only use the second one without visualization for all scenarios.
* Launch the simulation model with visualization
```
    $ python model_viz.py
```
* Launch the simulation model without visualization
```
    $ python model_run.py
```

The model uses the the csv file [infrastructure.csv](model/input/infrastructure.csv) to generate the model. The file contains the information about the bridges and the road segments.The intersections were generated in the [generate_intersections.ipynb](notebook/G09-A2-generate_intersections.ipynb) notebook. The notebook also contains the code to generate the [infrastructure.csv](model/input/infrastructure.csv) file.
The repository also contains the Jupyter Notebook file [model_output.ipynb](notebook/G09-A3-visualize_results.ipynb) which can be used to analyze the data collected during the simulation. The notebook contains all the code to reproduce the results presented in the report.

Further information about model specifc files can be found in the [model/README.md](model/README.md) file.