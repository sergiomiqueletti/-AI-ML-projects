import numpy as np


def train_model(X, y):
    """Train a simple linear regression model using the normal equation."""
    X_b = np.c_[np.ones((X.shape[0], 1)), X]
    theta = np.linalg.pinv(X_b.T @ X_b) @ X_b.T @ y
    return theta


def predict(X, theta):
    """Make predictions using the trained model parameters."""
    X_b = np.c_[np.ones((X.shape[0], 1)), X]
    return X_b @ theta


def normalize(X):
    """Normalize features to zero mean and unit variance."""
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    return (X - mean) / (std + 1e-8), mean, std


def mean_squared_error(y_true, y_pred):
    """Calculate Mean Squared Error between true and predicted values."""
    return np.mean((y_true - y_pred) ** 2)


if __name__ == "__main__":
    np.random.seed(42)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)

    theta = train_model(X, y)
    print(f"Model parameters: intercept={theta[0][0]:.2f}, slope={theta[1][0]:.2f}")

    y_pred = predict(X, theta)
    mse = mean_squared_error(y, y_pred)
    print(f"Training MSE: {mse:.4f}")

    X_new = np.array([[0], [1], [2]])
    predictions = predict(X_new, theta)
    print(f"Predictions for X=0,1,2: {predictions.flatten()}")
