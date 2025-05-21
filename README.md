# CARB

## Introduction

This project focuses on scraping football match data, specifically corner kicks, from ESPN and performing statistical analysis on it. The primary goal is to collect and analyze corner kick data to identify patterns and potentially gain insights for predictive modeling.

## Main Scripts and Data

*   **`ESPN_functions.py`**: This is the core script responsible for scraping match data from ESPN. It includes functions for fetching web pages, parsing HTML content, and extracting relevant information such as match details and corner kick counts. It also handles data cleaning and formatting before saving it.
*   **`ESPN_chisquared.py`**: This script performs statistical analysis, specifically chi-squared tests, on the collected corner kick data. It utilizes the data stored in `corners_append.csv` to test hypotheses about corner kick distributions and relationships between different match variables.
*   **`corners_append.csv`**: This CSV file is the primary data store for the project. All scraped and processed corner kick data is appended to this file.

## Jupyter Notebooks

The project also includes Jupyter Notebooks (`.ipynb` files) located in the `ipython notebooks/` directory. These notebooks are used for various purposes, including:

*   Exploratory data analysis.
*   Developing and testing scraping logic.
*   Visualizing data and analysis results.

## Key Python Dependencies

The project relies on the following key Python libraries:

*   `requests`: For making HTTP requests to fetch web pages.
*   `pandas`: For data manipulation and analysis, particularly for handling the `corners_append.csv` file.
*   `numpy`: For numerical computations, often used in conjunction with pandas.
*   `scipy`: For statistical functions, including the chi-squared test used in `ESPN_chisquared.py`.
*   `lxml`: For parsing HTML and XML content.

## Data Flow

The general data flow in this project is as follows:

1.  **Scraping**: `ESPN_functions.py` is used to scrape match data (primarily corner kicks) from ESPN.
2.  **Data Storage**: The scraped and processed data is appended to the `corners_append.csv` file.
3.  **Analysis**: `ESPN_chisquared.py` and the Jupyter notebooks use the data in `corners_append.csv` to perform statistical analysis and gain insights.
