import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from gluonts.dataset.common import ListDataset
from gluonts.torch.model.deepar import DeepAREstimator

# Title and Description
st.title("Time Series Forecasting with DeepAR")
st.write("This app demonstrates time series forecasting using the DeepAR model from GluonTS.")

# Load data
@st.cache
def load_data():
    url = (
        "https://raw.githubusercontent.com/AileenNielsen/"
        "TimeSeriesAnalysisWithPython/master/data/AirPassengers.csv"
    )
    df = pd.read_csv(url, index_col=0, parse_dates=True)
    return df

df = load_data()

# Display data
st.subheader("Air Passengers Dataset")
st.write("Below is a sample of the dataset used for forecasting:")
st.dataframe(df.head())

# Prepare dataset for GluonTS
dataset = ListDataset(
    [{"start": df.index[0], "target": df["#Passengers"].values}],
    freq="M",
)

# Model Configuration
st.sidebar.header("Model Configuration")
prediction_length = st.sidebar.slider("Prediction Length", 1, 24, 12)
max_epochs = st.sidebar.slider("Training Epochs", 1, 20, 5)

# Train Model
st.write("Training the model...")
training_data = dataset
test_data = ListDataset(
    [{"start": df.index[-36], "target": df["#Passengers"][-36:].values}],
    freq="M",
)

model = DeepAREstimator(
    prediction_length=prediction_length, freq="M", trainer_kwargs={"max_epochs": max_epochs}
).train(training_data)

# Predict
st.write("Generating forecasts...")
forecasts = list(model.predict(test_data))

# Plot Predictions
st.subheader("Forecasts")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df["1954":], color="black", label="True Values")
for forecast in forecasts:
    forecast.plot(ax=ax, color="blue")  # Remove `alpha` argument
ax.legend(loc="upper left", fontsize="large")
ax.set_title("True Values and Forecasts")
ax.set_xlabel("Time")
ax.set_ylabel("Passengers")
st.pyplot(fig)

# Footer
st.write("Developed with Streamlit.")
