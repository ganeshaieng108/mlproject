# Student Performance Predictor

An end-to-end machine learning application that predicts a student's math score based on demographic and academic background factors. The project covers the complete ML lifecycle — from data ingestion and preprocessing to model training, evaluation, and deployment via a Flask web application.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [ML Pipeline](#ml-pipeline)
- [Web Interface](#web-interface)
- [Deployment](#deployment)
- [Future Improvements](#future-improvements)

---

## Overview

This project is built to demonstrate a production-style machine learning workflow. Given inputs like a student's gender, race/ethnicity, parental education level, lunch type, test preparation status, and reading/writing scores, the model predicts their expected math score.

The goal was not just to train a model but to build the entire system around it — clean pipelines, modular code, a trained artifact saved to disk, and a web interface that non-technical users can interact with.

---

## Project Structure

```
├── src/
│   ├── components/
│   │   ├── data_ingestion.py       # Loads and splits raw data
│   │   ├── data_transformation.py  # Feature engineering and preprocessing
│   │   └── model_trainer.py        # Model selection and training
│   ├── pipeline/
│   │   ├── predict_pipeline.py     # Inference pipeline used by the web app
│   │   └── train_pipeline.py       # Orchestrates end-to-end training
│   ├── exception.py                # Custom exception handling
│   ├── logger.py                   # Centralized logging
│   └── utils.py                    # Helper functions (save/load model, evaluate)
├── artifacts/                      # Saved model, preprocessor, and datasets
├── templates/
│   ├── index.html                  # Landing page
│   └── home.html                   # Prediction form and results
├── app.py                          # Flask app entry point (development)
├── application.py                  # Flask app entry point (production/AWS)
├── setup.py                        # Package setup
├── requirements.txt                # Project dependencies
└── README.md
```

---

## Tech Stack

- **Language:** Python 3.8+
- **Web Framework:** Flask
- **ML Libraries:** scikit-learn, XGBoost, CatBoost
- **Data Processing:** pandas, NumPy
- **Serialization:** dill
- **Visualization:** matplotlib, seaborn (EDA)
- **Deployment:** AWS Elastic Beanstalk

---

## Features

- Modular, component-based ML pipeline (ingestion → transformation → training)
- Automated model selection across multiple algorithms with hyperparameter tuning
- Custom exception handling and structured logging throughout the codebase
- Preprocessing artifacts (scaler, encoder) saved alongside the model for consistent inference
- Flask web app with a form-based UI for real-time predictions
- `setup.py` configured for packaging the `src` module, following standard Python project conventions

---

## Getting Started

### Prerequisites

- Python 3.8 or above
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/student-performance-predictor.git
cd student-performance-predictor

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> The `-e .` line in `requirements.txt` (currently commented out) installs the `src` package in editable mode. Uncomment it if you want `from src.x import y` imports to resolve without path hacks.

### Running the Application

```bash
# Train the model first (generates artifacts/)
python src/pipeline/train_pipeline.py

# Start the Flask development server
python app.py
```

Navigate to `http://localhost:5000` in your browser.

---

## ML Pipeline

The training pipeline is broken into three independent components:

**1. Data Ingestion**
Reads the raw dataset, performs a train-test split, and saves both splits to the `artifacts/` directory.

**2. Data Transformation**
Builds a `ColumnTransformer` that applies:
- `StandardScaler` on numerical features (reading score, writing score)
- `OneHotEncoder` on categorical features (gender, race/ethnicity, etc.)

The fitted preprocessor object is serialized to disk using `dill` so it can be reused identically during inference.

**3. Model Trainer**
Trains multiple regression models (Ridge, Random Forest, XGBoost, CatBoost, etc.) and evaluates each using R² score on the test set. The best-performing model is saved to `artifacts/model.pkl`.

---

## Web Interface

The Flask app exposes two routes:

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/predictdata` | GET | Renders the prediction form |
| `/predictdata` | POST | Accepts form input, runs inference, returns predicted score |

On form submission, a `CustomData` object is created from the inputs, converted to a DataFrame, passed through the saved preprocessor, and then fed to the saved model. The predicted math score is rendered back on the page.

---

## Deployment

The project is structured for deployment on **AWS Elastic Beanstalk**. `application.py` is the entry point used by Elastic Beanstalk (it looks for a callable named `application` by default, which is why both files exist — `app.py` for local development and `application.py` for AWS).

To deploy:
1. Zip the project (excluding `venv/`, `artifacts/`, and `__pycache__/`)
2. Create a new Elastic Beanstalk environment (Python platform)
3. Upload the zip and let EB handle the rest

---

## Future Improvements

- Add a CI/CD pipeline using GitHub Actions for automated testing and deployment
- Containerize the application with Docker for consistent environment management
- Integrate MLflow for experiment tracking and model versioning
- Add input validation on the frontend and backend to handle edge cases gracefully
- Expand the dataset and explore deep learning approaches for comparison
