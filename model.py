import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    unnamed_cols = [c for c in df.columns if c.strip() == "" or c.startswith("Unnamed")]
    df = df.drop(columns=unnamed_cols)
    if "Listing_Date" in df.columns:
        df = df.drop(columns=["Listing_Date"])
    df = df.dropna(subset=["Price_EUR"])
    return df


def build_model(X):
    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
    categorical_features = X.select_dtypes(include=["object", "bool"]).columns

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    return Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ])


def evaluate_model(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mse)
    return mse, r2, rmse


def plot_predictions(y_true, y_pred, save_path="predicted_vs_actual.png"):
    plt.figure(figsize=(8, 6))
    plt.scatter(y_true, y_pred, alpha=0.6)
    plt.xlabel("Actual Price (EUR)")
    plt.ylabel("Predicted Price (EUR)")
    plt.title("Madrid Housing Prices — Predicted vs Actual")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Plot saved to {save_path}")


def plot_predictions_with_reference(y_true, y_pred, save_path="predicted_vs_actual_line.png"):
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())

    plt.figure(figsize=(8, 6))
    plt.scatter(y_true, y_pred, alpha=0.6)
    plt.plot([min_val, max_val], [min_val, max_val], color="red", linewidth=2)
    plt.xlabel("Actual Price (EUR)")
    plt.ylabel("Predicted Price (EUR)")
    plt.title("Predicted vs Actual (with perfect line)")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Plot saved to {save_path}")


def main():
    df = load_data("madrid_housing_dataset.csv")
    print("Dataset shape:", df.shape)
    print(df.head())
    print(df.dtypes)

    target = "Price_EUR"
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training data: {X_train.shape}, {y_train.shape}")
    print(f"Testing data: {X_test.shape}, {y_test.shape}")

    model = build_model(X)
    model.fit(X_train, y_train)
    print("Model trained successfully.")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        y_pred = model.predict(X_test)
    print("Predicted Prices (first 10):", y_pred[:10])
    print("Actual Prices (first 10):", y_test.values[:10])

    mse, r2, rmse = evaluate_model(y_test, y_pred)
    print(f"Mean Squared Error (MSE): {mse:,.2f}")
    print(f"R-squared (R²): {r2:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:,.2f} EUR")

    plot_predictions(y_test, y_pred)
    plot_predictions_with_reference(y_test, y_pred)


if __name__ == "__main__":
    main()
