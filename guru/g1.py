import numpy as np
from plotly.io import show
from sklearn.model_selection import train_test_split
from skfolio import Population, RiskMeasure
from skfolio.datasets import load_sp500_dataset
from skfolio.optimization import InverseVolatility, MeanRisk, ObjectiveFunction
from skfolio.preprocessing import prices_to_returns

try:
    prices = load_sp500_dataset()
    X = prices_to_returns(prices)
    X_train, X_test = train_test_split(X, test_size=0.3, shuffle=False)

    # Explicitly enforce long-only and full investment
    model = MeanRisk(
        risk_measure=RiskMeasure.VARIANCE,
        objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
        portfolio_params=dict(name="Max Sharpe"),
        min_weights=0.0,  # No short positions
    )
    model.fit(X_train)

    benchmark = InverseVolatility(portfolio_params=dict(name="Inverse Vol"))
    benchmark.fit(X_train)

    pred_model, pred_bench = model.predict(X_test), benchmark.predict(X_test)
    population = Population([pred_model, pred_bench])
    show(population.plot_cumulative_returns())

except Exception as e:
    print(f"An error occurred: {e}")