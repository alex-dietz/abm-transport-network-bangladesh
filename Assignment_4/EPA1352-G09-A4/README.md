# Assignment 4

Created by: EPA1352 Group 09 

| Name    | Student Number |
|:-------:|:--------|
| Alexander Dietz  | 5859549 | 
| Ryan Tan Yi Wei | 5708427 |
| Ludwig Branzk | 5862515 |
| Corné Snoeij | 5174473 |
| Ariel Goldin | 5354717 |


## Introduction

This repository analyzes the vulnerability, criticality, and importance of road segments and bridges in Bangladesh. It combines traffic, flooding, and bridge data to assess the vulnerability, criticality, and importance. A report can be found in the [report](report) folder describing the methodology as well as the results of the analysis.

## How to Use
The repository consists functionally of two notebooks:
- [G09-A4-data_preparation.ipynb](notebook/G09-A4-data_preparation.ipynb): This notebook contains the code to prepare the data for the analysis. It parses the road data to extract the traffic information and the uses this in combination with other data sources to calculate the vulnerability, criticality, and importance of the road segments and bridges. The results are saved to the data folder.
- [G09-A4-analysis.ipynb](notebook/G09-A4_analysis.ipynb): This notebook contains the code to analyze the data. It contains the code to load the processed data, to perform the analysis. The notebook is divided by Vulnerability, Criticality, and Importance. It provides a top 10 of road segments and bridges and visualizes the geospatial data.

You can run the notebooks with jupyter or inside an IDE, like VS Code.

# Folder Structure
The repository is structured as follows:
- [data](data): Contains the data used for the analysis.
- [notebook](notebook): Contains the notebooks used for the analysis.
- [report](report): Contains the report of the analysis.