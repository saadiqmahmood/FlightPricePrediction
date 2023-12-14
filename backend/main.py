import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os

# Set the working directory to the root of your project.
# This ensures that all file paths are relative to the project root.
os.chdir('C:/Users/Saadiq Mahmood/OneDrive/UA92/FlightPricePrediction')

# DATA COLLECTION 
# Load the dataset from a CSV file.
# The dataset is expected to be in the 'data' folder within the project directory.
file_path = 'backend/flight_dataset.csv'
data = pd.read_csv(file_path)

# Data Cleaning
# Remove the 'Unnamed: 0' column from the dataset.
# This column is often an artifact of saving/loading data with pandas and is usually not needed.
data.drop(['Unnamed: 0'], axis=1, inplace=True)

# DATA PREPROCESSING

class CustomLabelEncoder:
    def __init__(self):
        # Initialize an empty dictionary to store the mapping of labels to integers.
        self.label_map = {}

    def fit(self, data):
        # Extract unique labels from the data and create a mapping to integers.
        unique_labels = set(data)
        self.label_map = {label: idx for idx, label in enumerate(unique_labels)}
        # Add an 'unknown' label for handling unseen labels during transformation.
        self.label_map['unknown'] = len(unique_labels)

    def transform(self, data):
        # Transform labels in the data to integers using the label_map.
        # Unseen labels are mapped to 'unknown'.
        return [self.label_map.get(label, self.label_map['unknown']) for label in data]

    def fit_transform(self, data):
        # Fit the encoder and transform the data in one step.
        self.fit(data)
        return self.transform(data)

# Define categorical and numerical columns in the dataset.
categorical_columns = ['airline', 'source_city', 'flight', 'arrival_time', 'departure_time', 'stops', 'destination_city', 'class']
numerical_columns = ['days_left', 'duration']

# Initialize a dictionary to store CustomLabelEncoders for each categorical column.
label_encoders = {}

# Encode each categorical column using CustomLabelEncoder.
for column in categorical_columns:
    encoder = CustomLabelEncoder()
    data[column] = encoder.fit_transform(data[column])
    label_encoders[column] = encoder

# Scale numerical features using MinMaxScaler for normalization.
scaler = MinMaxScaler()
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# DATA PREPARATION

# Separate the features and the target variable from the dataset.
# 'Price' is the target variable we want to predict.
X = data.drop('price', axis=1)  # Features (independent variables)
y = data['price']  # Target variable (dependent variable)

# Splitting the dataset into training and testing sets.
# The test set is 20% of the total dataset, and the split is reproducible with the random_state.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the test data to CSV files for later use or evaluation.
# This is useful for ensuring the model is tested on the same data across different runs or platforms.
X_test.to_csv('data/X_test.csv', index=False)
y_test.to_csv('data/y_test.csv', index=False)


# MODEL TRAINING

# Initialize the Random Forest Regressor.
# Random Forest is chosen for its robustness and ability to handle non-linear data.
model = RandomForestRegressor(random_state=42)
# Train the model using the training data.
model.fit(X_train, y_train)

# Save the trained model to a file for later use or deployment.
# This allows the model to be loaded and used without retraining.
joblib.dump(model, 'backend/random_forest_model.pkl')

# Save the label encoders and scaler.
# These are necessary for preprocessing new data in the same way as the training data.
joblib.dump(label_encoders, 'backend/label_encoder.pkl')
joblib.dump(scaler, 'backend/min_max_scaler.pkl')

# Save the mappings from the label encoders.
# This is useful for understanding how categorical variables were encoded.
encoder_mappings = {col: encoder.label_map for col, encoder in label_encoders.items()}
joblib.dump(encoder_mappings, 'backend/label_encoder_mappings.pkl')


