# Milk Optimization Project

## Project Title

**Design and Implementation of an Intelligent Cattle Feed Recommendation and Cost Optimization System for Maximizing Milk and Meat Production Using Random Forest Algorithm**

## Project Overview

The Milk Optimization Project is a machine learning based web application built to help cattle farmers estimate milk production from feed composition and animal information.

The system takes inputs such as maize, soybean meal, hay, groundnut cake, protein level, fiber level, energy level, cattle breed, age, and weight. It then uses a trained Random Forest regression model to predict expected milk yield.

The project also gives a simple cost optimization summary by estimating the current feed cost, an optimized cost, percentage savings, and monthly savings. The frontend dashboard is built with Streamlit and includes charts for feed composition, production trends, cost summary, and model performance.

## Main Problem The Project Solves

Many cattle farmers still rely on guesswork when deciding feed combinations for better milk production. This can lead to high feed costs, poor nutrient balance, and unstable milk output.

This project provides a smarter way to support feed planning by using historical cattle feed data and machine learning to estimate how different feed and animal conditions may affect milk yield.

## Main Objectives

1. To build a machine learning model that predicts milk yield from cattle feed and animal data.
2. To create a simple dashboard where users can enter feed and cattle details.
3. To estimate feed cost and possible cost savings.
4. To visualize feed composition and production information.
5. To support better decision making for cattle feed planning.

## How The Project Works

The project has two major parts:

### 1. Model Training

The `train.py` file loads the dataset from:

```text
data/cattle_feed_dataset.csv
```

It uses the following input features:

```text
maize
soybean
hay
pkc
protein
fiber
energy
breed
age
weight
```

The target variable is:

```text
milk_yield
```

The cattle breed column is converted from text to numbers using `LabelEncoder`. After that, the dataset is split into training and testing data. A `RandomForestRegressor` is trained and saved as:

```text
model/random_forest_model.pkl
```

The breed encoder is also saved as:

```text
model/breed_encoder.pkl
```

### 2. Streamlit Web App

The `app.py` file loads the saved model and encoder. The user enters feed values and cattle details from the sidebar. The app converts the selected breed into the encoded value, sends all inputs to the model, and returns a predicted milk yield.

The dashboard also calculates:

```text
Feed cost
Optimized cost
Monthly savings
Estimated meat gain
```

## Important Note About The Current Version

The machine learning model currently predicts **milk yield** only.

The meat gain shown in the dashboard is calculated using this formula:

```python
meat_gain = prediction * 0.18
```

So, meat gain is not currently predicted by a separate machine learning model. For a stronger final-year or academic version, you can train a second model using `weight_gain` as the target variable.

Also, the cost optimization is currently formula based. It assumes optimized cost is 82% of the current cost:

```python
optimized_cost = feed_cost * 0.82
```

This means the project performs prediction and simple cost estimation. It is not yet doing advanced mathematical optimization.

## Project Folder Structure

Use this exact folder structure:

```text
milk_optimization_project/
│
├── app.py
├── train.py
├── requirements.txt
├── README.md
│
├── data/
│   └── cattle_feed_dataset.csv
│
└── model/
    ├── breed_encoder.pkl
    └── random_forest_model.pkl
```

This structure is important because both `app.py` and `train.py` depend on these paths.

## Dataset Description

The dataset contains 10,000 records and 13 columns.

### Input Columns

| Column | Meaning |
|---|---|
| maize | Percentage of maize in the feed mixture |
| soybean | Percentage of soybean meal in the feed mixture |
| hay | Percentage of hay in the feed mixture |
| pkc | Percentage of palm kernel cake or groundnut cake used in the feed mixture |
| protein | Protein content of the feed |
| fiber | Fiber content of the feed |
| energy | Energy level of the feed |
| breed | Cattle breed |
| age | Age of the cattle |
| weight | Weight of the cattle in kg |

### Output Columns

| Column | Meaning |
|---|---|
| milk_yield | Milk production output used as the main prediction target |
| weight_gain | Animal weight gain output that can be used for future model training |
| cost | Feed cost value in the dataset |

## Technologies Used

| Tool | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data loading and processing |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning model training |
| Random Forest Regressor | Milk yield prediction model |
| Joblib | Saving and loading model files |
| Streamlit | Web application dashboard |
| Plotly | Interactive charts and visualizations |

## Step By Step Setup

### Step 1: Install Python

Install Python 3.10 or above.

To check if Python is installed, run:

```bash
python --version
```

or:

```bash
python3 --version
```

### Step 2: Open The Project Folder

Open your terminal or command prompt and move into the project folder:

```bash
cd milk_optimization_project
```

### Step 3: Create A Virtual Environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install The Required Libraries

Run:

```bash
pip install -r requirements.txt
```

The requirements include:

```text
pandas
numpy
scikit-learn==1.4.2
streamlit
plotly
joblib
```

The `scikit-learn==1.4.2` version is recommended because the uploaded model files were created with that version. Using a much newer version may show a model loading warning.

### Step 5: Run The Streamlit App

Run:

```bash
streamlit run app.py
```

After running the command, Streamlit will open the app in your browser.

If it does not open automatically, copy the local URL from your terminal and paste it into your browser.

## How To Use The App

1. Open the Streamlit app.
2. Use the sidebar to enter feed values.
3. Select the cattle breed.
4. Enter cattle age and weight.
5. The system predicts milk production.
6. The dashboard shows feed composition, estimated feed cost, optimized cost, monthly savings, and production charts.

## How To Retrain The Model

Retraining is useful when you update the dataset or want to improve the model.

Make sure your dataset is inside:

```text
data/cattle_feed_dataset.csv
```

Then run:

```bash
python train.py
```

This will:

1. Load the dataset.
2. Encode the breed column.
3. Train the Random Forest model.
4. Evaluate the model using MAE, MSE, RMSE, and R² score.
5. Print feature importance.
6. Save the new model and encoder into the `model` folder.

## Model Explanation In Simple Terms

Random Forest is a machine learning algorithm that combines many decision trees.

A single decision tree makes predictions by asking questions about the data. For example:

```text
Is protein high?
Is energy level high?
Is cattle weight above a certain value?
Is the breed Holstein?
```

Random Forest builds many trees and combines their answers. This usually gives a more stable and accurate prediction than one tree alone.

In this project, the Random Forest model studies the relationship between feed composition, animal features, and milk yield. When a new feed combination is entered, it estimates the likely milk production.

## Cost Calculation Used In The App

The app estimates feed cost using this formula:

```python
feed_cost = maize * 4 + soybean * 9 + hay * 2 + pkc * 3 + minerals * 5
```

Then it estimates optimized cost as:

```python
optimized_cost = feed_cost * 0.82
```

Monthly savings is calculated as:

```python
monthly_savings = (feed_cost - optimized_cost) * 30
```

## Common Errors And Fixes

### Error: FileNotFoundError

This usually means the file structure is wrong.

Make sure you have:

```text
model/random_forest_model.pkl
model/breed_encoder.pkl
data/cattle_feed_dataset.csv
```

Do not leave the files with names like:

```text
random_forest_model(1).pkl
breed_encoder(1).pkl
cattle_feed_dataset(1).csv
```

Rename them or place them correctly.

### Error: No module named streamlit

Run:

```bash
pip install streamlit
```

or reinstall all requirements:

```bash
pip install -r requirements.txt
```

### Warning: InconsistentVersionWarning

This means your installed scikit-learn version is different from the version used to create the saved model.

Install the recommended version:

```bash
pip install scikit-learn==1.4.2
```

or retrain the model with your current scikit-learn version:

```bash
python train.py
```

## Suggested Improvements

1. Train a second model for `weight_gain` instead of calculating meat gain from milk prediction.
2. Use the real `cost` column from the dataset for stronger cost prediction.
3. Add mathematical optimization to recommend the best feed mixture under a fixed budget.
4. Add user authentication for farmers or farm managers.
5. Add a database to store cattle records and prediction history.
6. Add downloadable reports for farm decision making.
7. Add live feed price updates.
8. Add charts comparing predicted milk yield against actual milk yield.
9. Add validation so total feed percentage does not exceed 100%.
10. Deploy the app online using Streamlit Community Cloud, Render, or Hugging Face Spaces.

## Academic Defense Summary

This project uses machine learning to support cattle feed planning and milk production estimation. It collects feed composition and cattle details from the user, processes them through a trained Random Forest regression model, and predicts expected milk yield. The system also estimates feed cost and possible savings, allowing farmers to make better decisions on feed usage and production planning.

The main value of the project is that it reduces dependence on guesswork and gives a data driven approach to cattle feed recommendation and cost management.

## Author

Faith Abiodun
