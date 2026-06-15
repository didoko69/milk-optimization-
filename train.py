import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ============================================
# LOAD DATASET
# ============================================

data = pd.read_csv("data/cattle_feed_dataset.csv")

print("Dataset Loaded Successfully")
print(data.head())

# ============================================
# ENCODE CATEGORICAL DATA
# ============================================

encoder = LabelEncoder()

data['breed'] = encoder.fit_transform(data['breed'])

# Save encoder
joblib.dump(encoder, "model/breed_encoder.pkl")

# ============================================
# FEATURES & TARGET
# ============================================

X = data[
    [
        'maize',
        'soybean',
        'hay',
        'pkc',
        'protein',
        'fiber',
        'energy',
        'breed',
        'age',
        'weight'
    ]
]

# TARGET VARIABLE
# Change to weight_gain if needed

y = data['milk_yield']

# ============================================
# SPLIT DATA
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# ============================================
# BUILD RANDOM FOREST MODEL
# ============================================

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

# ============================================
# TRAIN MODEL
# ============================================

print("\nTraining Model...")

model.fit(X_train, y_train)

print("Model Training Completed")

# ============================================
# PREDICTIONS
# ============================================

predictions = model.predict(X_test)

# ============================================
# EVALUATION
# ============================================

mae = mean_absolute_error(y_test, predictions)

mse = mean_squared_error(y_test, predictions)

rmse = mse ** 0.5

r2 = r2_score(y_test, predictions)

print("\n=========== MODEL PERFORMANCE ===========")

print(f"MAE  : {mae:.4f}")

print(f"MSE  : {mse:.4f}")

print(f"RMSE : {rmse:.4f}")

print(f"R2   : {r2:.4f}")

# ============================================
# FEATURE IMPORTANCE
# ============================================

feature_names = X.columns

importance = model.feature_importances_

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importance
})

importance_df = importance_df.sort_values(
    by='Importance',
    ascending=False
)

print("\n=========== FEATURE IMPORTANCE ===========")

print(importance_df)

# ============================================
# SAVE MODEL
# ============================================

joblib.dump(
    model,
    "model/random_forest_model.pkl"
)

print("\nModel Saved Successfully")