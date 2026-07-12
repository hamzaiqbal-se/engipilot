import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
import joblib
import os

FEATURE_COLUMNS = [
    "completion_rate",
    "blocked_ratio",
    "velocity",
    "days_elapsed",
    "days_to_deadline",
    "avg_workload_ratio",
]

os.makedirs("agents/models", exist_ok=True)

PARAM_DISTRIBUTIONS = {
    "n_estimators": [100, 150, 200, 300],
    "max_depth": [2, 3, 4, 5],
    "learning_rate": [0.01, 0.03, 0.05, 0.1],
    "subsample": [0.6, 0.7, 0.8, 0.9],
    "colsample_bytree": [0.6, 0.7, 0.8, 0.9],
    "reg_alpha": [0.1, 0.5, 1.0],
    "reg_lambda": [0.5, 1.0, 2.0],
}


def train_and_save(target_column: str, model_filename: str):
    df = pd.read_csv("scripts/training_data.csv")

    X = df[FEATURE_COLUMNS]
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Further split train into train/validation for early stopping
    X_train_sub, X_val, y_train_sub, y_val = train_test_split(X_train, y_train, test_size=0.15, random_state=42)

    # --- Step 1: Hyperparameter search (lightweight, 20 candidate combinations) ---
    base_model = XGBRegressor(random_state=42)
    search = RandomizedSearchCV(
        base_model,
        param_distributions=PARAM_DISTRIBUTIONS,
        n_iter=20,
        scoring="r2",
        cv=3,
        random_state=42,
        n_jobs=-1,
    )
    search.fit(X_train_sub, y_train_sub)
    best_params = search.best_params_
    print(f"\n--- {target_column}: Best hyperparameters found ---")
    print(best_params)

    # --- Step 2: Retrain best model with early stopping on a validation set ---
    final_model = XGBRegressor(
        **best_params,
        random_state=42,
        early_stopping_rounds=15,
        eval_metric="mae",
    )
    final_model.fit(
        X_train_sub, y_train_sub,
        eval_set=[(X_val, y_val)],
        verbose=False,
    )

    print(f"Best iteration (early stopping): {final_model.best_iteration}")

    # --- Step 3: Evaluate on train and test ---
    train_preds = final_model.predict(X_train)
    test_preds = final_model.predict(X_test)

    train_mae = mean_absolute_error(y_train, train_preds)
    test_mae = mean_absolute_error(y_test, test_preds)
    train_r2 = r2_score(y_train, train_preds)
    test_r2 = r2_score(y_test, test_preds)

    print(f"Train MAE: {train_mae:.4f}  |  Test MAE: {test_mae:.4f}")
    print(f"Train R²:  {train_r2:.4f}  |  Test R²:  {test_r2:.4f}")

    gap = train_r2 - test_r2
    if gap > 0.1:
        print(f"⚠️  WARNING: Train-Test R² gap is {gap:.4f} — possible overfitting.")
    else:
        print(f"✅ Train-Test R² gap is {gap:.4f} — model generalizes well.")

    joblib.dump(final_model, f"agents/models/{model_filename}")
    print(f"Saved model to agents/models/{model_filename}")


if __name__ == "__main__":
    train_and_save("delay_risk", "delay_risk_model.pkl")
    train_and_save("burnout_risk", "burnout_risk_model.pkl")