# Big Data Visualization Project - Team 3 - CS524




```markdown
# UV Index Dashboard: Data Visualization, Forecasting, and Analysis

## Table of Contents
- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Dataset Overview](#dataset-overview)
- [Research Challenges](#research-challenges)
- [Features](#features)
- [Getting Started](#getting-started)
- [How to Run the Project](#how-to-run-the-project)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction
The UV Index Dashboard is an interactive platform for visualizing, forecasting, and analyzing UV Index data across different geographical locations in the United States. Built using Python and Dash, this project leverages machine learning models and statistical techniques to provide actionable insights into UV exposure and its potential risks.

---

## Problem Statement
UV radiation plays a critical role in public health, agriculture, and climate studies. Excessive UV exposure is a leading cause of skin damage and other health issues, while insufficient exposure can lead to Vitamin D deficiency. This dashboard addresses the challenge of understanding and forecasting UV Index trends by:
1. Providing detailed visualizations of historical and real-time UV data.
2. Utilizing machine learning models for predictive analysis.
3. Offering insights into derived factors like cloud impact and ozone protection.

Understanding UV Index variations can help mitigate health risks, support policymaking, and enhance awareness about UV safety.

---

## Dataset Overview
The project uses the following datasets:
- UV Index Data (`todaysdata.csv`):
  - Contains daily UV Index measurements, including clear sky and cloudy sky conditions.
  - Includes related meteorological factors like cloud transmission, aerosol transmission, and total column ozone.
- Geographical Data (`us-states.json`):
  - GeoJSON file used for interactive map visualizations.
  
### Key Fields in the Data:
- `Date`: Measurement date in YYYYMMDD format.
- `NAME`: State name.
- `Clear Sky UVI`: UV Index under clear sky conditions.
- `Cloudy Sky UVI`: UV Index under cloudy sky conditions.
- `Cloud Transmission`: Percentage of sunlight transmitted through clouds.
- `Total Column Ozone`: Ozone concentration in the atmosphere.
- `Solar Zenith Angle`: Angle between the sun and the observer's zenith.

---

## Research Challenges
1. Data Cleaning and Integration: Handling missing or inconsistent data across multiple features.
2. Model Adaptation: Tailoring machine learning models (e.g., Prophet, Linear Regression) to work with seasonal and location-specific variations in UV Index.
3. Derived Factors: Calculating and interpreting derived metrics like UV attenuation, ozone protection, and transmission efficiency.
4. Visualization Design: Creating interactive and user-friendly visualizations to ensure accessibility for diverse users.

---

## Features
### Home Page
- Central hub with links to different sections of the application.

### UV Index Visualizations
- Interactive choropleth maps showing UV Index trends across the United States.
- State-specific bar and line charts for detailed visual analysis.

### Machine Learning Forecasting
- Regression-based predictions for UV Index using key influencing factors.
- Prophet-based time-series forecasting for long-term trends.

### Derived Factor Calculations
- Analyze UV attenuation, ozone protection, and other derived factors.
- Visualize trends and variations over time for selected regions.

---

## Getting Started
### Prerequisites
Ensure you have the following installed:
1. Python 3.8+
2. Required Python libraries:
   - `dash`
   - `dash-bootstrap-components`
   - `pandas`
   - `numpy`
   - `scikit-learn`
   - `plotly`
   - `prophet`

### Installation
1. Clone the repository.
2. Install dependencies:
   pip install -r requirements.txt

## How to Run the Project
1. Start the Dash server:
   python app.py
2. Open your browser and navigate to:
   http://127.0.0.1:8050/

3. Explore the following pages:
   - UV Index Visualizations: Interactive maps and state-specific charts.
   - Regression Analysis: Predictive models using influencing factors.
   - Forecasting: Time-series analysis using Prophet.
   - Derived Factors: Calculate and visualize advanced UV-related metrics.

---

## Results
### Highlights
1. Visualization Insights:
   - Clear temporal and geographical patterns in UV Index data.
   - Monthly and seasonal trends derived from machine learning models.

2. Forecasting Accuracy:
   - Time-series predictions using Prophet with confidence intervals.
   - Regression models highlighting the impact of key factors on UV Index.

3. Derived Factors:
   - Insights into ozone protection, cloud impact, and solar energy potential.
   - Quantitative metrics to support decision-making in UV safety.

---
