# LOGISIGHT Last-Mile Delivery Intelligence

## FA-2: Dashboarding and Deployment

**Course:** Mathematics for AI-II\
**CRS:** Artificial Intelligence\
**Assessment:** Formative Assessment 2 --- Dashboarding and Deployment\
**Project Title:** Analyzing Last-Mile Delivery Data for Performance
Insights\
**Organization / Scenario:** LogiSight Analytics Pvt. Ltd.\
**Student:** M Raksmi Priyasree\
**Programme:** IBCP-XII (Year 2)\
**WACP ID:** 1000405

------------------------------------------------------------------------

## 1. Project Overview

LogiSight is an interactive last-mile delivery analytics dashboard
designed to help logistics managers understand delivery performance and
investigate the factors associated with delays.

The project transforms the dashboard plan created in FA-1 into a working
Python and Streamlit application. The dashboard processes the delivery
dataset with Pandas, creates derived analytical variables, calculates
delivery-performance metrics, and presents interactive visualizations
using Plotly.

The application allows managers to:

-   View overall delivery-performance KPIs.
-   Investigate the effect of weather and traffic on delivery time.
-   Compare average delivery performance across vehicle types.
-   Explore relationships between agent rating, agent age, and delivery
    time.
-   Identify areas with higher average delivery times.
-   Compare delivery-time distributions across product categories.
-   Explore delivery performance by time of day.
-   Investigate the relationship between delivery distance and delivery
    time.
-   Investigate the relationship between pickup duration and total
    delivery time.
-   Filter the dashboard by weather, traffic, vehicle, category, area,
    and order date.
-   Compare the dashboard state before and after applying filters.

The final application is intended to provide a clear path from:

**Raw Delivery Data → Data Preparation → Analysis → Visualization →
Insight → Managerial Decision**

------------------------------------------------------------------------

# 2. Business Problem

Last-mile delivery performance can be affected by several operational
and environmental factors. Logistics managers need to understand where
delays occur and which factors are associated with slower delivery
performance.

The dashboard addresses questions such as:

1.  How do weather and traffic affect average delivery time?
2.  Which vehicle type has the shortest average delivery time?
3.  How do agent rating and age relate to delivery time?
4.  Which areas have the highest average delivery times?
5.  Which product categories have the highest and most variable delivery
    times?
6.  Does the time of day when an order is placed influence delivery
    performance?
7.  Does pickup duration influence the overall delivery time?
8.  Does delivery distance correspond to delivery time?

These questions are explored using grouped summaries, distributions,
scatter plots, derived variables, and interactive filters.

------------------------------------------------------------------------

# 3. Dataset

The project uses the provided **Last mile Delivery Data.csv** dataset.

The dataset contains approximately **43,739 delivery records** and **16
columns**.

### Dataset fields

  Field               Purpose
  ------------------- -----------------------------------
  `Order_ID`          Unique order identifier
  
  `Agent_Age`         Age of the delivery agent
  
  `Agent_Rating`      Delivery-agent rating
  
  `Store_Latitude`    Store latitude
  
  `Store_Longitude`   Store longitude
  
  `Drop_Latitude`     Delivery/drop latitude
  
  `Drop_Longitude`    Delivery/drop longitude
  
  `Order_Date`        Date of the order
  
  `Order_Time`        Time when the order was placed
  
  `Pickup_Time`       Time when the order was picked up
  
  `Weather`           Weather condition
  
  `Traffic`           Traffic condition
  
  `Vehicle`           Vehicle type
  
  `Area`              Delivery area
  
  `Delivery_Time`     Overall delivery time
  
  `Category`          Product category
  

The dataset is used as the source for all dashboard calculations and
visualizations.

------------------------------------------------------------------------

# 4. Technology Stack

The project is implemented in Python.

### Main technologies

-   **Python** --- application and analytical logic
-   **Pandas** --- data loading, cleaning, transformation, grouping, and
    aggregation
-   **NumPy** --- numerical calculations, including Haversine distance
-   **Plotly Express** --- interactive charts
-   **Streamlit** --- dashboard interface and deployment
-   **GitHub** --- source-code repository and version control
-   **Streamlit Cloud** --- public deployment

### Python dependencies

The project uses the following packages:

``` text
streamlit
pandas
numpy
plotly
statsmodels
```

`statsmodels` is used by Plotly's OLS trendline functionality for
relationship analysis.

------------------------------------------------------------------------

# 5. Project Structure

### File descriptions

#### `app.py`

Contains the complete Streamlit application, including:

-   Page configuration
-   Styling
-   Dataset loading
-   Data cleaning
-   Derived-variable creation
-   Filtering
-   KPI calculations
-   Plotly visualizations
-   Navigation
-   Interactive controls
-   Business insights
-   Error handling

#### `requirements.txt`

Contains the Python libraries required to run the application.

#### `Last mile Delivery Data.csv`

The source dataset used by the dashboard.

#### `mascot.png`

LogiSight mascot image displayed in the dashboard.

------------------------------------------------------------------------

# 6. Data Cleaning & Preparation

The application performs data preparation programmatically using Pandas
when it starts.

This ensures that the same cleaning and transformation process is
applied every time the dashboard runs.

## 6.1 Column-name cleaning

Column names are stripped of leading and trailing spaces to avoid errors
caused by inconsistent formatting.


------------------------------------------------------------------------

## 6.2 Text-field cleaning

Important categorical fields are converted to Pandas string values and
stripped of unnecessary spaces.

The cleaned categorical fields include:

-   `Order_ID`
-   `Weather`
-   `Traffic`
-   `Vehicle`
-   `Area`
-   `Category`

This improves consistency when filtering and grouping.

------------------------------------------------------------------------

## 6.3 Numeric conversion

The following fields are converted to numeric values:

-   `Agent_Age`
-   `Agent_Rating`
-   `Store_Latitude`
-   `Store_Longitude`
-   `Drop_Latitude`
-   `Drop_Longitude`
-   `Delivery_Time`

Invalid numeric values are converted to missing values using
`errors="coerce"`.

------------------------------------------------------------------------

## 6.4 Date conversion

`Order_Date` is converted to a Pandas datetime field.

Invalid date values are safely converted to missing values.

------------------------------------------------------------------------

## 6.5 Combining date and time

The dashboard combines:

-   `Order_Date` + `Order_Time`
-   `Order_Date` + `Pickup_Time`

to create:

-   `Order_DateTime`
-   `Pickup_DateTime`

These calculated datetime fields are required for pickup-duration and
time-of-day analysis.

------------------------------------------------------------------------

## 6.6 Delivery-time validation

Rows without a valid `Delivery_Time` are removed.

Negative delivery times are also removed because a negative delivery
duration is not meaningful for this analysis.

------------------------------------------------------------------------

# 7. Derived Variables

The dashboard creates several calculated fields that are not directly
present in the original CSV.

## 7.1 Order Hour

`Order_Hour` is extracted from the order datetime.

This supports time-of-day analysis.

------------------------------------------------------------------------

## 7.2 Time of Day

Orders are grouped into four time periods:

  Hour range   Time of Day
  ------------ -------------
  00--05       Night
  06--11       Morning
  12--16       Afternoon
  17--23       Evening

Derived field:

``` text
Time_of_Day
```

This allows delivery performance to be compared across broad periods of
the day.

------------------------------------------------------------------------

## 7.3 Pickup Duration

Pickup duration is calculated as:

``` text
Pickup_Duration = Pickup_DateTime − Order_DateTime
```

The result is converted to minutes.

Negative pickup durations are treated as invalid and changed to missing
values.

This variable supports the Pickup Efficiency analysis.

------------------------------------------------------------------------

## 7.4 Delivery Distance

Delivery distance is calculated from the store and drop coordinates
using the Haversine formula.

Inputs:

``` text
Store_Latitude
Store_Longitude
Drop_Latitude
Drop_Longitude
```

Output:

``` text
Delivery_Distance
```

The result is expressed in kilometres.

This provides an additional way to investigate whether longer delivery
routes correspond to longer delivery times.

------------------------------------------------------------------------

## 7.5 Agent Age Group

Agents are grouped into:

-   `<25`
-   `25–40`
-   `40+`

Derived field:

``` text
Agent_Age_Group
```

This is used to group the Agent Performance scatter plot.

------------------------------------------------------------------------

## 7.6 Late Delivery

A late-delivery threshold is calculated as:

``` text
Mean Delivery Time + 1 × Standard Deviation
```

A delivery is classified as late when:

``` text
Delivery_Time > Late Threshold
```

Derived field:

``` text
Late_Delivery
```

This Boolean field is used to calculate the late delivery rate.

------------------------------------------------------------------------

# 8. Key Performance Indicators

The dashboard displays four main KPIs.

## Average Delivery Time

The mean of `Delivery_Time` for the current filtered dataset.

This gives managers an overall view of delivery speed.

------------------------------------------------------------------------

## Total Deliveries

The number of records in the current filtered view.

This shows the size of the segment being analyzed.

------------------------------------------------------------------------

## Late Delivery Rate

Calculated as:

``` text
Number of Late Deliveries
÷
Total Deliveries
× 100
```

The late status is based on the mean + one standard deviation threshold
described above.

------------------------------------------------------------------------

## Late Threshold

The dashboard displays the calculated threshold in minutes.

This allows the user to understand the benchmark used for identifying
unusually long deliveries.

------------------------------------------------------------------------

# 9. Interactive Filtering

The dashboard provides a dedicated control panel for filtering.

Available filters:

-   Weather
-   Traffic
-   Vehicle
-   Category
-   Area
-   Order Date

The filter workflow is:

``` text
Select filters
      ↓
Click Apply Filters
      ↓
Filter dataset
      ↓
Recalculate KPIs
      ↓
Update visualizations
      ↓
Interpret filtered results
```

The application uses a Streamlit form so that users can make multiple
selections before applying them.

A **Reset Filters** control restores the full dataset view.

------------------------------------------------------------------------

# 10. Before → After Filter Impact

One additional interaction in the dashboard compares the previous
selected state with the newly filtered state.

After applying filters, the application calculates:

-   Previous average delivery time
-   Current average delivery time
-   Change in minutes
-   Percentage change
-   Previous late delivery rate
-   Current late delivery rate

This provides immediate feedback about how the selected segment differs
from the previous view.

Example interpretation:

``` text
Previous average → Current average
Previous late rate → Current late rate
```

This helps managers understand whether a selected operational segment
performs better or worse than the previous segment.

------------------------------------------------------------------------

# 11. Dashboard Navigation

The application contains the following analytical pages:

1.  Overview
2.  Executive Insights
3.  Probability & Risk
4.  Delay Analyzer
5.  Vehicle Comparison
6.  Agent Performance
7.  Area Analysis
8.  Category Analysis
9.  Time-of-Day
10. Distance Analyzer
11. Pickup Efficiency

The navigation is located in the left-side application rail.

The dashboard uses a wide layout with:

-   navigation on the left
-   analysis in the center
-   filters on the right

This layout keeps the manager's workflow visible while preserving space
for charts.

------------------------------------------------------------------------

# 12. Compulsory Visualizations

The FA-2 brief requires five core visualizations.

## 12.1 Delay Analyzer

### Business question

**How do weather and traffic affect average delivery time?**

### Visualization

Grouped bar chart showing:

``` text
Weather
×
Traffic
→
Average Delivery Time
```

Weather categories are compared across traffic conditions.

### Data used

-   `Weather`
-   `Traffic`
-   `Delivery_Time`

### Business purpose

The chart allows managers to compare delivery performance under
different environmental and traffic conditions and investigate
situations associated with longer delivery times.

------------------------------------------------------------------------

# 13. Vehicle Comparison

### Business question

**Which vehicle type has the shortest average delivery time?**

### Visualization

Bar chart showing:

``` text
Vehicle
→
Average Delivery Time
```

Vehicle categories are grouped and sorted by average delivery time.

### Data used

-   `Vehicle`
-   `Delivery_Time`

### Business purpose

The analysis helps managers compare fleet performance and consider
vehicle allocation for different operating conditions.

------------------------------------------------------------------------

# 14. Agent Performance

### Business question

**How do agent rating and age relate to delivery time?**

### Visualization

Scatter plot:

``` text
X-axis → Agent Rating
Y-axis → Delivery Time
Group → Agent Age Group
```

Age groups:

-   `<25`
-   `25–40`
-   `40+`

The dashboard also calculates the correlation between agent rating and
delivery time for the current filtered selection.

### Data used

-   `Agent_Rating`
-   `Agent_Age`
-   `Delivery_Time`

### Business purpose

The analysis helps explore workforce-performance patterns that may be
useful for training, staffing, and performance-management decisions.

### Important interpretation note

A correlation or visual pattern does not by itself prove that age or
rating causes delivery performance differences. The dashboard therefore
treats this as exploratory relationship analysis.

------------------------------------------------------------------------

# 15. Area Analysis

### Business question

**Which areas have the highest average delivery times?**

### Visualization

Horizontal bar chart:

``` text
Area
→
Average Delivery Time
```

Areas are ranked by average delivery time.

### Data used

-   `Area`
-   `Delivery_Time`

### Business purpose

This helps managers identify locations with relatively high delivery
times and investigate potential regional bottlenecks.

------------------------------------------------------------------------

# 16. Category Analysis

### Business question

**Which categories have the highest and most variable delivery times?**

### Visualization

Boxplot showing the distribution of delivery time for each product
category.

The visualization allows comparison of:

-   median
-   spread
-   variability
-   distribution
-   unusually high observations

### Data used

-   `Category`
-   `Delivery_Time`

### Additional statistics

The dashboard calculates:

-   mean
-   standard deviation
-   median
-   number of deliveries

It identifies the category with:

-   highest average delivery time
-   greatest variability

### Business purpose

This helps managers investigate whether certain categories have
different delivery requirements or greater variability in delivery
performance.

------------------------------------------------------------------------

# 17. Optional / Additional Visualizations

In addition to the five compulsory visualizations, the dashboard
includes analyses based on the derived variables planned during FA-1.

## 17.1 Time-of-Day Analyzer

Compares average delivery time across:

-   Night
-   Morning
-   Afternoon
-   Evening

This is derived from `Order_Time`.

------------------------------------------------------------------------

## 17.2 Distance Analyzer

Compares:

``` text
Delivery Distance
vs
Delivery Time
```

using a scatter plot and OLS trendline.

The dashboard also displays the correlation between the two variables.

------------------------------------------------------------------------

## 17.3 Pickup Efficiency Analyzer

Compares:

``` text
Pickup Duration
vs
Delivery Time
```

using a scatter plot and OLS trendline.

The dashboard displays the correlation between pickup duration and
delivery time.

------------------------------------------------------------------------


## 17.4 Executive Insights

The dashboard includes an **Executive Insights** page that automatically summarizes important patterns from the currently selected dataset.

It highlights:

- Average delivery time
- Late delivery rate
- Late-delivery threshold
- Slowest weather-and-traffic combination
- Fastest vehicle type
- Slowest-performing area
- Category with the highest late-delivery rate
- Correlation between agent rating and delivery time

The page also provides stakeholder-oriented notes for:

- **Managers** — areas and operating conditions that may require attention
- **Operations teams** — vehicle, pickup, distance, and time-of-day factors to investigate
- **Senior stakeholders / investors** — consistency, scalability, and operational risk

The page concludes with recommended operational actions based on the observed data patterns.

---

## 17.5 Probability & Risk Analyzer

The dashboard includes a **Probability & Risk** page that estimates the historical probability of a delivery being late for a selected scenario.

The analysis uses:

``` text
P(Late | Selected Scenario)
=
Number of Late Deliveries
÷
Total Deliveries
```

Users can independently select:

- Weather
- Traffic
- Vehicle
- Area
- Category

The page displays:

- Historical late-delivery probability
- Risk level
- Number of comparable deliveries
- Number of late deliveries
- On-time versus late probability
- Factor-level risk information

Risk levels are classified as:

- **HIGH** — 60% or above
- **MODERATE** — 30% to below 60%
- **LOW** — below 30%

This is an **empirical historical probability based on the available dataset**, not a machine-learning prediction.


# 18. Plot Design & Usability

The application uses Plotly for interactive visualizations.

Charts are designed to include:

-   clear titles
-   readable axis labels
-   consistent units
-   hover information
-   appropriate grouping
-   meaningful legends
-   consistent dark-theme styling
-   sufficient spacing around chart titles

Large scatter plots are sampled to a maximum of approximately 7,000
points when necessary to keep the dashboard responsive while retaining
the overall pattern of the data.

------------------------------------------------------------------------

# 19. Application UI Design

The dashboard uses a premium dark interface.

### Main visual characteristics

-   Deep charcoal background
-   Forest green accents
-   Burgundy highlights
-   Muted champagne/gold details
-   Cream-colored typography
-   Rounded analytical panels
-   Clear navigation
-   Right-side control panel
-   Large central charts

The design follows the structure developed during FA-1 while adapting it
into a working Streamlit interface.

------------------------------------------------------------------------

# 20. Mascot

The dashboard supports an optional mascot image.

The mascot is intended as a visual brand element rather than an
analytical feature.

------------------------------------------------------------------------

# 21. Running the Application Locally

## Step 1 --- Install Python

Use a current Python 3 environment.

## Step 2 --- Clone or download the repository

Example:

``` bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd logisight-fa2
```

## Step 3 --- Install dependencies

``` bash
pip install -r requirements.txt
```

## Step 4 --- Make sure the dataset is present

Place:

``` text
Last mile Delivery Data.csv
```

in the same folder as `app.py`.

The application also supports a `data/` directory.

## Step 5 --- Run Streamlit

``` bash
streamlit run app.py
```

The application will open in the browser.

------------------------------------------------------------------------

# 22. GitHub Deployment

The project is intended to be hosted in a GitHub repository.


``` text
app.py
requirements.txt
Last mile Delivery Data.csv
README.md
```

The mascot is stored in:

``` text
mascot.png
```

------------------------------------------------------------------------

# 23. Streamlit Cloud Deployment

The final application is intended to be deployed through Streamlit
Cloud.

General deployment workflow:

``` text
GitHub Repository
       ↓
Streamlit Cloud
       ↓
Select Repository
       ↓
Select app.py
       ↓
Deploy
       ↓
Public Dashboard URL
```

The deployed application should use:

``` text
app.py
```

as its main application file.

`requirements.txt` tells Streamlit Cloud which Python packages need to
be installed.

------------------------------------------------------------------------

# 24. Deployed Application

**Streamlit Cloud:**\
Replace this section with the final public deployment URL.

``` text
PASTE YOUR STREAMLIT CLOUD URL HERE
```

The final submitted version should contain the working public URL
required by the assessment.

------------------------------------------------------------------------

# 25. GitHub Repository

**GitHub Repository:**\
Replace this section with the final repository URL.

``` text
PASTE YOUR GITHUB REPOSITORY URL HERE
```

The repository should be publicly accessible or shared according to the
school's submission requirements.

------------------------------------------------------------------------

# 26. How the Dashboard Supports Managers

The dashboard is designed around a question-driven workflow.

### Step 1 --- Start with KPIs

Managers see:

-   Average Delivery Time
-   Total Deliveries
-   Late Delivery Rate
-   Late Threshold

### Step 2 --- Select a business question

Examples:

-   Why are deliveries slower in certain conditions?
-   Which vehicle performs fastest?
-   Are there differences between areas?
-   Which categories have greater variability?

### Step 3 --- Refine the segment

Managers can use:

-   Weather
-   Traffic
-   Vehicle
-   Category
-   Area
-   Order Date

### Step 4 --- Apply filters

The dashboard updates the selected dataset.

### Step 5 --- Read the visualization

Charts provide comparisons, distributions, or relationships.

### Step 6 --- Identify patterns

Managers can look for:

-   higher average delivery times
-   differences between groups
-   variability
-   possible bottlenecks
-   relationships between variables

### Step 7 --- Make an operational decision

Potential actions include:

-   reviewing resource allocation
-   investigating high-delay areas
-   adjusting fleet allocation
-   improving pickup processes
-   planning resources around high-delay periods
-   identifying training or staffing areas

The dashboard is intended to support decisions rather than replace
managerial judgment.

------------------------------------------------------------------------

# 27. Data Logic

The complete analytical pipeline is:

``` text
RAW CSV DATA
      ↓
LOAD DATA WITH PANDAS
      ↓
INSPECT & CLEAN DATA
      ↓
HANDLE INVALID / MISSING VALUES
      ↓
SELECT RELEVANT VARIABLES
      ↓
CREATE DERIVED VARIABLES
      ↓
APPLY USER FILTERS
      ↓
GROUP & AGGREGATE DATA
      ↓
CALCULATE KPIs
      ↓
GENERATE PLOTLY VISUALIZATIONS
      ↓
IDENTIFY PATTERNS
      ↓
INTERPRET RESULTS
      ↓
SUPPORT MANAGERIAL DECISIONS
```

This is the implementation of the data logic planned in FA-1.

------------------------------------------------------------------------

# 28. Relationship Analysis

Two additional analyses use correlation and OLS trendlines:

## Agent Rating vs Delivery Time

Used to explore whether agent rating is associated with delivery time.

## Delivery Distance vs Delivery Time

Used to explore whether longer calculated routes correspond to longer
delivery times.

## Pickup Duration vs Delivery Time

Used to explore whether longer pickup durations are associated with
longer overall delivery times.

These are exploratory analyses.

A relationship in the data should not automatically be interpreted as
causation.

------------------------------------------------------------------------

# 29. Handling Empty Filter Results

Because the dashboard is interactive, users can select combinations of
filters that return little or no data.

The application checks for insufficient data before generating certain
analyses.

When there is not enough data, the dashboard displays a warning rather
than producing an invalid chart.

This improves usability and prevents misleading visualizations.

------------------------------------------------------------------------

# 30. Performance Considerations

The dataset contains tens of thousands of records, so some
visualizations can contain many points.

For scatter plots, the application limits the plotted sample to
approximately 7,000 records using a fixed random state.

This keeps the interface responsive while preserving the overall
relationship pattern.

Grouped charts use Pandas aggregation before visualization so that
Plotly receives summarized data rather than unnecessary raw rows.

------------------------------------------------------------------------

# 31. Limitations

The dashboard is an analytical decision-support tool and has several
limitations.

### 1. Association is not causation

A relationship between two variables does not prove that one variable
causes another.

### 2. Historical data

The dashboard analyzes the provided delivery dataset. It does not
automatically obtain live traffic, weather, GPS, or external logistics
data.

### 3. Derived distance

Delivery distance is calculated from store and drop coordinates using
the Haversine formula. This represents geographic straight-line distance
rather than the exact road route distance.

### 4. Late-delivery threshold

Late delivery is defined using:

``` text
Mean Delivery Time + 1 Standard Deviation
```

This is an analytical threshold selected for the project and does not
necessarily represent the company's official SLA.

### 5. Missing values

Invalid or unavailable values may be excluded from specific analyses
when they are required for the calculation.

### 6. Filtered interpretation

Some results can change significantly when filters are applied. Managers
should consider the number of records in the selected segment before
making decisions.

------------------------------------------------------------------------

# 32. Assessment Alignment

The FA-2 brief focuses on three major areas:

## Data Cleaning & Preparation

The application:

-   loads the CSV with Pandas
-   cleans field formats
-   handles invalid values
-   prepares dates and times
-   creates derived variables
-   calculates average delivery time
-   calculates late delivery rate
-   calculates the late threshold
-   groups data for visualizations

## Planned Visualizations

The five compulsory analyses are implemented:

-   Delay Analyzer
-   Vehicle Comparison
-   Agent Performance Scatter Plot
-   Area Analysis
-   Category Visualizer / Boxplot

Additional analyses include:

-   Time-of-Day
-   Distance
-   Pickup Efficiency

## Streamlit Interface & Deployment

The application includes:

-   interactive filters
-   KPI cards
-   navigation
-   dynamic charts
-   filter application
-   reset controls
-   before/after filter comparison
-   responsive layout
-   GitHub-ready Python code
-   `requirements.txt`
-   Streamlit Cloud deployment structure

------------------------------------------------------------------------

# 33. Reproducibility

The project is designed so that the dashboard can be reproduced by:

1.  Obtaining the repository.
2.  Installing `requirements.txt`.
3.  Placing the dataset in the expected location.
4.  Running `streamlit run app.py`.

All major data-preparation steps are performed inside the application
rather than relying on manual spreadsheet editing.

This makes the analytical process repeatable.

------------------------------------------------------------------------

# 34. Future Improvements

Possible future extensions include:

-   monthly delivery trend analysis
-   more detailed late-delivery breakdowns
-   route-based road distance instead of straight-line distance
-   live weather and traffic integration
-   predictive delivery-time modelling
-   delivery-time forecasting
-   anomaly detection
-   automated alerts for high-delay conditions
-   additional geographic mapping
-   role-based dashboards for different logistics teams

These features are outside the core FA-2 implementation but could extend
the project into a more advanced logistics intelligence platform.

------------------------------------------------------------------------

# 35. Conclusion

LogiSight converts the last-mile delivery dataset into an interactive
analytics dashboard designed around real operational questions.

The project demonstrates the complete workflow:

``` text
Data
→
Cleaning
→
Transformation
→
Metrics
→
Visualization
→
Interaction
→
Insight
→
Decision
```

By combining Python, Pandas, NumPy, Plotly, and Streamlit, the project
turns the FA-1 storyboard into a working dashboard that allows logistics
managers to investigate delivery performance from multiple perspectives.

The final objective is simple:

> **Same Data. Smarter Decisions.**

------------------------------------------------------------------------

# 36. References & Learning Resources

The FA-2 brief identifies the following resources for learning and
support:

-   DataCamp --- Streamlit tutorials
-   Streamlit --- official documentation
-   GitHub --- repository hosting
-   DataCamp --- Python data cleaning
-   freeCodeCamp --- Pandas data cleaning and preprocessing
-   DataCamp --- Plotly Express
-   Seaborn documentation
-   Matplotlib documentation
-   Streamlit dashboard development articles
-   Streamlit widget API documentation

These resources were used as learning references for understanding
Python data preparation, visualization, Streamlit interfaces, and
deployment.

------------------------------------------------------------------------

# 37. Credits

**Project:** LogiSight --- Last-Mile Delivery Intelligence\
**Assessment:** Mathematics for AI-II --- FA-2\
**Scenario:** LogiSight Analytics Pvt. Ltd.\
**Student:** M Raksmi Priyasree\
**Programme:** IBCP-XII (Year 2)\
**WACP ID:** 1000405

------------------------------------------------------------------------

