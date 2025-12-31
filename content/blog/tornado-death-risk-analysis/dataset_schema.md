+++
title = "Tornado Analysis Dataset Schema"
date = 2025-12-31
description = "Schema documentation for the tornado death risk analysis dataset."
+++

# Dataset Schema

This document describes the data structure used in the Tornado Death Risk Analysis.

## Source Data Structure

The analysis uses a CSV-formatted dataset with the following columns:

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `Year`      | Integer   | The calendar year of the record (1900-2024). |
| `Deaths`    | Integer   | Total confirmed tornado-related fatalities in the United States for the given year. |
| `PopFactor` | Float     | Estimated population (in millions) across 25 tornado-prone states*. |
| `Era`       | String    | Historical classification of the period: 'Pre-Radar', 'Warning Era', or 'Modern Era'. |

## Derived Fields

The analysis script calculates the following additional metric:

| Column Name | Data Type | Formula | Description |
|-------------|-----------|---------|-------------|
| `DeathRate` | Float     | `Deaths / PopFactor` | Population-adjusted mortality rate (deaths per million people in tornado-prone regions). |

## *Tornado-Prone States
The `PopFactor` includes population estimates for: AL, AR, FL, GA, IA, IL, IN, KS, KY, LA, MI, MN, MO, MS, NC, ND, NE, OH, OK, SC, SD, TN, TX, VA, WI.

## Data Sources
- **Tornado Deaths (1950-2024):** NOAA Storm Prediction Center
- **Tornado Deaths (1900-1949):** Thomas P. Grazulis, "Significant Tornadoes"
- **Population:** U.S. Census Bureau Historical Population Estimates
