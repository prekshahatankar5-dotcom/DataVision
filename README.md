# DataVision – Data Analytics Platform

**Turn Your Data Into Meaningful Insights.**

DataVision is a Python-based data analytics platform designed to make data analysis simple and accessible. It allows users to upload datasets, explore information, clean data, create interactive visualizations, and discover useful insights.

## About the Project

DataVision combines a Flask web application with a Streamlit dashboard to provide an easy-to-use data analysis experience.

## Key Features

- **Data Upload:** Upload CSV and Excel datasets.
- **Dataset Overview:** View rows, columns, missing values, and duplicate records.
- **Data Preview:** Explore uploaded datasets.
- **Data Cleaning:** Handle missing values and remove duplicate records.
- **Data Filtering:** Filter numerical and categorical data.
- **Interactive Visualization:** Generate charts and graphs.
- **Smart Insights:** Discover useful patterns in datasets.
- **Report Downloads:** Download cleaned datasets and analysis reports.

## Technologies Used

- Python
- Flask
- Streamlit
- Pandas
- Plotly
- HTML
- CSS

## Project Structure

```text
DataVision/
│
├── app.py
├── dashboard.py
├── README.md
├── .gitignore
│
├── static/
│   └── style.css
│
└── templates/
    └── index.html
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/prekshahatankar5-dotcom/DataVision.git
```

**2. Open the project folder**

```bash
cd DataVision
```

**3. Install the required libraries**

```bash
pip install flask streamlit pandas plotly openpyxl
```

**4. Run the Flask application**

```bash
python app.py
```

Open your browser at:

`http://127.0.0.1:5000`

**5. Run the Streamlit dashboard**

Open another terminal and run:

```bash
streamlit run dashboard.py
```

Open:

`http://localhost:8501`

## Project Objective

The objective of DataVision is to help users understand and analyze their datasets through a simple interface, without needing complicated data analysis tools.

## Future Improvements

- Add advanced data analysis features.
- Improve dashboard design and user experience.
- Introduce machine learning-based predictions.
- Deploy the application online.

---

**Developed as a Data Analytics Project using Python, Flask, and Streamlit.**