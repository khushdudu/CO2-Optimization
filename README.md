# Machine Learning Model for CO2 Emissions Prediction

## Table of Contents
1. [Business Use Case](#business-use-case)
2. [Dataset Description](#dataset-description)
3. [Baseline Model](#baseline-model)
    - Features and Preprocessing
    - Validation Strategy
    - Metrics Obtained
4. [First Iteration](#first-iteration)
    - Changes Made
    - Impact on Metrics
5. [Serving the Model](#serving-the-model)


## Business Use Case

Context: In recent years, the aviation industry has faced increasing pressure to reduce its environmental impact, particularly in terms of **carbon emissions**. Airlines are exploring ways to reduce their **CO2 footprint** as governments, regulatory bodies, and environmentally conscious customers demand more sustainable air travel. With **Sustainable Aviation Fuel (SAF)** emerging as a potential alternative to traditional **Jet A-1 fuel**, there is growing interest in optimizing its usage to minimize CO2 emissions without compromising on fuel efficiency or increasing operational costs.

In this project, we aim to build a machine learning model to predict **CO2 emissions** for flights based on various factors such as distance, fuel consumption, altitude, etc. The project is particularly relevant in the context of exploring the use of **Sustainable Aviation Fuel (SAF)** and traditional **Jet A-1 fuel** to estimate how emissions can be reduced over different flight routes. The ultimate goal is to optimize the ratio of SAF to Jet A-1 fuel to lower CO2 emissions while maintaining performance.


## Dataset Description

The dataset used in this project contains approximately **2000-3000 flight records**, with the following key features:

- **Distance (km)**: The distance traveled by the flight.
- **Cruising Altitude (ft)**: The altitude at which the flight operates.
- **Wind Speed (km/h)**: Wind speed during the flight.
- **Fuel Consumption (liters)**: The amount of fuel consumed by the flight.
- **SAF Percentage (%)**: The percentage of Sustainable Aviation Fuel used.
- **Jet A-1 Percentage (%)**: The percentage of Jet A-1 fuel used.
- **CO2 Emissions (g)**: The target variable representing CO2 emissions in grams.

### Dataset Preprocessing

- **Handling Missing Values**: No missing values were present in the dataset.
- **Outliers**: Outliers were capped based on the 1st and 99th percentiles to avoid extreme values affecting the model.
- **Scaling**: Features were standardized using **StandardScaler** to ensure all variables are on the same scale.
- **Categorical Variables**: Not applicable as all features were numerical.


## Baseline Model

### Features and Preprocessing
For the baseline model, we used the following features:

- Distance (km)
- Cruising Altitude (ft)
- Wind Speed (km/h)
- Fuel Consumption (liters)
- Passenger Load
- Cargo Load (kg)
- SAF Percentage
- Jet A-1 Percentage

The **CO2 Emissions** column was our target variable, and we first converted it from kilograms (kg) to grams (g) for more precision in modeling.

### Model Used

For the baseline model, we used **Ridge Regression** with **5-fold cross-validation** to ensure that the model generalized well to unseen data.

### Validation Strategy

- We used **80% of the data for training** and **20% for testing**.
- **5-fold cross-validation** was employed during training to reduce the variance in performance and to ensure robust results.

### Metrics Obtained

| Model             | RMSE (Test)  | Cross-Validation RMSE |
|-------------------|--------------|-----------------------|
| Ridge Regression  | 0.168        | 0.176                 |

The Ridge Regression model performed well with an **RMSE of 0.168** on the test set and **0.176** across 5-fold cross-validation.


## First Iteration

### Changes Made

- **Explored more complex models**: After analyzing the residuals, we realized that the Ridge Regression model did not capture some of the non-linear relationships in the data, especially at the higher end of CO2 emissions. We decided to try **Random Forest**, **Gradient Boosting**, and **XGBoost** to capture non-linear patterns and improve predictive accuracy.
- **Random Forest**: Added randomness and decision tree-based modeling to capture non-linearity.
- **Gradient Boosting & XGBoost**: Focused on iteratively improving the model by combining weak learners (decision trees) and adjusting errors.

### Impact on Metrics

After training and testing these models, we compared the results:

| Model             | RMSE (Test)  | Cross-Validation RMSE |
|-------------------|--------------|-----------------------|
| Ridge Regression  | 0.168        | 0.176                 |
| Random Forest     | 0.165        | 0.173                 |
| Gradient Boosting | 0.163        | 0.171                 |
| XGBoost           | 0.162        | 0.170                 |

The **XGBoost model** showed the best performance with an **RMSE of 0.162** on the test set and **0.170** across cross-validation folds. This improvement came from the ability of tree-based models to capture non-linear relationships that were missed by the linear Ridge Regression model.


## Serving the Model

Once the model was optimized, it was **deployed using an HTTP API** built with **Flask**. The API accepts input data via a POST request and returns the predicted CO2 emissions for a given flight.

The model was containerized using **Docker** to ensure portability and ease of deployment. Instructions for running the model locally inside a Docker container are as follows:

### Running the Model Locally

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-repo-url
    cd your-repo-url
    ```

2. **Build the Docker image**:

    ```bash
    docker build -t ml-api .
    ```

3. **Run the Docker container**:

    ```bash
    docker run -p 5000:5000 ml-api
    ```

4. **Test the API** by sending a POST request:

    ```bash
    curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"Distance (km)": 1500, "Fuel Consumption (liters)": 2000, ...}'
    ```


### Conclusion
This project successfully built and deployed a machine learning model for CO2 emissions prediction using flight data. Through iterative improvements and model comparisons, we achieved optimal results with **XGBoost**. The model is now available via an API for real-time predictions, with the entire application containerized using Docker for easy deployment.

