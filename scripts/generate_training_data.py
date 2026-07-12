import pandas as pd
import numpy as np

np.random.seed(42)

def generate_synthetic_data(n_samples: int = 5000) -> pd.DataFrame:
    """
    Generates synthetic project-sprint feature data with realistic patterns
    for training the Risk Agent's prediction models.
    """
    data = {
        "completion_rate": np.random.beta(2, 2, n_samples),
        "blocked_ratio": np.random.beta(1, 5, n_samples),
        "velocity": np.random.gamma(2, 1.5, n_samples),
        "days_elapsed": np.random.randint(1, 60, n_samples),
        "days_to_deadline": np.random.randint(-10, 30, n_samples),
        "avg_workload_ratio": np.random.beta(2, 2, n_samples) * 1.5,
    }
    df = pd.DataFrame(data)

    # --- Delay risk label ---
    delay_score = (
        (1 - df["completion_rate"]) * 0.4
        + df["blocked_ratio"] * 0.35
        + (df["days_to_deadline"] < 5).astype(int) * 0.25
    )
    # Slightly higher noise = more realistic, harder to perfectly memorize -> discourages overfitting
    df["delay_risk"] = (delay_score + np.random.normal(0, 0.08, n_samples)).clip(0, 1)

    # --- Burnout risk label ---
    burnout_score = (
        df["avg_workload_ratio"].clip(0, 1.5) / 1.5 * 0.6
        + (df["velocity"] > df["velocity"].quantile(0.75)).astype(int) * 0.4
    )
    df["burnout_risk"] = (burnout_score + np.random.normal(0, 0.08, n_samples)).clip(0, 1)

    return df


if __name__ == "__main__":
    df = generate_synthetic_data()
    df.to_csv("scripts/training_data.csv", index=False)
    print(f"Generated {len(df)} rows. Saved to scripts/training_data.csv")
    print(df.describe())