
![image](https://github.com/user-attachments/assets/9ff2ba1f-7f2f-4718-9017-02ea8dd75d2e)


# ✈️ **Flight Fare Prediction**


This project focuses on predicting flight ticket prices based on various features such as airline, source, destination, duration, and other travel-related information. The objective is to help users get a price estimate and make better booking decisions.

# Project Objective:
The objective of this project is to analyse flight fare data by applying SQL techniques, perform data cleaning and exploratory data analysis (EDA) using SQL, and then build a predictive model using machine learning to estimate flight ticket prices based on various travel-related features.

# 📌 **Project Overview**
**Domain:** Travel & Aviation

**Goal:** Predict the fare of a flight using historical flight data

**Approach:** Started by performing data cleaning and exploratory data analysis (EDA) using SQL, followed by feature engineering and building machine learning models in Python.

**Tools Used:**

- SQL: For data cleaning and exploratory data analysis (EDA)

- Python: For model building and evaluation

- Pandas, NumPy, Matplotlib, Seaborn: For preprocessing and visualisation

- Scikit-learn, LinearRegression, DecisionTreeRegressor , RandomForestRegressor

# **About data**

1. **Airline** : 	The name of the airline (e.g., IndiGo, Air India, SpiceJet). Different airlines have different pricing strategies.
2. **Date_of_Journey** :	The date on which the passenger is scheduled to fly. Can be split into day, month, and year for analysis.
3. **Source** :	The city from which the flight departs (e.g., Delhi, Mumbai).
4. **Destination** :	The city where the flight is landing.
5 **Route** :	The route taken by the flight, sometimes with stops (e.g., DEL → BOM → BLR). This can give information about layovers.
6. **Dep_Time** :	Departure time of the flight. Can be broken into hour and minute or part of day (Morning, Afternoon, Evening).
7. **Arrival_Time** :	Time at which the flight arrives at the destination. Similar to departure time, can be transformed.
8. **Duration** :	Total duration of the flight from source to destination.
9. **Total_Stops** :	Number of stops (e.g., non-stop, 1 stop, 2 stops). Usually, more stops mean cheaper flights.
10 **Additional_Info** :	Any extra info (e.g., "No info", "In-flight meal not included", etc.). Might affect pricing.
11 **Price** : The target variable. This is what you're trying to predict using the other features.


# **DATA CLEANING AND EXPLORATORY DATA ANALYSIS**

A step-by-step explanation of the data cleaning and EDA process can be found at this link, as carried out by me
https://drive.google.com/file/d/1dpIO2pC2_sxTTxstT1TvbGnLGkE9rvAu/view?usp=sharing


https://flightpriceprediction-gtvjjw47rnqnatnw6hhruc.streamlit.app/
![Streamlit-GoogleChrome2025-04-0823-20-36-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/6591f485-548d-43c3-bd93-e68dcfe48a22)


# **KEY INSIGHTS**

- Friday is the most expensive day to travel, followed by Sunday.

- Midnight is the cheapest time to fly due to low demand.

- Bangalore → New Delhi is the costliest route, while Chennai → Kolkata is the cheapest.

- Jet Airways Business class offers the highest fare, likely due to luxury services.

- A positive correlation exists between ticket price and duration.

- More stops often lead to higher fares, but not necessarily longer durations.

- May and June see the highest number of bookings, driven by vacation travel.


# **🛠 Tools Used**

- MySQL / PostgreSQL

- SQL Window Functions, CASE, Aggregations, Joins, CTEs

- Data pre-processing & formatting for temporal analysis







