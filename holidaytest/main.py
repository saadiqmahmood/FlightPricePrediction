import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os

# Set the working directory to the root of your project
os.chdir('C:/Users/Saadiq Mahmood/OneDrive/UA92/FlightPricePrediction')

# # DATA COLLECTION 
file_path = 'holidaytest/data/flight_holiday.csv'
data = pd.read_csv(file_path)
data.drop
# Drop the 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in data.columns:
    data.drop('Unnamed: 0', axis=1, inplace=True)

# Add a new column for holiday indicator
# Initially, set all values to 0 (non-holiday)
data['is_holiday'] = 0

# Define the holiday dates in terms of days_left
# Assuming February 11th is day 50 and March 31st is day 1
# Here, 'Manipur Holiday' is an example holiday from March 14th to 16th
holiday_dates = {
    'Manipur Holiday': range(17, 20)  # Range of days_left for the holiday
    # Additional holidays can be added to this dictionary
}

# Update the holiday indicator for the defined holidays
for holiday, days in holiday_dates.items():
    # If 'days_left' falls within the holiday range, set 'is_holiday' to 1
    data.loc[data['days_left'].isin(days), 'is_holiday'] = 1



# # DATA PREPROCESSING 
class CustomLabelEncoder:
    def __init__(self):
        # Initialize an empty dictionary to store the mapping of labels to integers.
        self.label_map = {}

    def fit(self, data):
        # Extract unique labels from the data.
        unique_labels = set(data)
        # Create a mapping from each label to a unique integer.
        # Enumerate starts from 0 and assigns an integer to each label.
        self.label_map = {label: idx for idx, label in enumerate(unique_labels)}
        # Add an 'unknown' label for handling any labels during transform 
        # that were not seen during fit.
        self.label_map['unknown'] = len(unique_labels)

    def transform(self, data):
        # Transform the input data (list of labels) into integers based on the label_map.
        # If a label is not found in label_map, it is replaced with the integer for 'unknown'.
        return [self.label_map.get(label, self.label_map['unknown']) for label in data]

    def fit_transform(self, data):
        # A convenience method that first fits the encoder to the data and then transforms the data.
        # This is useful for encoding training data in one step.
        self.fit(data)
        return self.transform(data)


# List of columns
categorical_columns = ['airline', 'flight', 'source_city', 'departure_time', 'stops', 'arrival_time','destination_city', 'class']
numerical_columns = ['duration', 'days_left', 'is_holiday']
# Initialize a dictionary to hold CustomLabelEncoders
label_encoders = {}

# Fit and transform each categorical column
for column in categorical_columns:
    encoder = CustomLabelEncoder()
    data[column] = encoder.fit_transform(data[column])
    label_encoders[column] = encoder

# Scaling numerical features
scaler = MinMaxScaler()
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# # DATA PREP
# 'Price' is the target variable
X = data.drop('price', axis=1)
y = data['price']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save test data
X_test.to_csv('holidaytest/data/X_test.csv', index=False)
y_test.to_csv('holidaytest/data/y_test.csv', index=False)

# # MODEL TRAINING
# Initialize the Random Forest Regressor
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'holidaytest/data/random_forest_model.pkl')
# Save label encoders and scaler
joblib.dump(label_encoders, 'holidaytest/data/label_encoder.pkl')
joblib.dump(scaler, 'holidaytest/data/min_max_scaler.pkl')
# Save encoder mappings
encoder_mappings = {col: encoder.label_map for col, encoder in label_encoders.items()}
joblib.dump(encoder_mappings, 'holidaytest/data/label_encoder_mappings.pkl')



