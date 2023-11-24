import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


# # DATA COLLECTION 
file_path = 'data/flight_dataset.csv'
data = pd.read_csv(file_path)

# # DATA PREPROCESSING 
# Assuming df is your DataFrame
categorical_columns = ['airline', 'flight', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class']

label_encoders = {}
for column in categorical_columns:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])
# Assuming 'duration' is a numerical feature
scaler = MinMaxScaler()
data['duration'] = scaler.fit_transform(data[['duration']])

# # MODEL BUILDING
# Initialize the Random Forest Regressor
model = RandomForestRegressor(random_state=42)

# # DATA PREP
# If 'Price' is the target variable
X = data.drop('price', axis=1)
y = data['price']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # MODEL TRAINING
model.fit(X_train, y_train)
# Save the trained model
joblib.dump(model, 'random_forest_model.pkl')
joblib.dump(label_encoders, 'label_encoder.pkl')
joblib.dump(scaler, 'min_max_scaler.pkl')

# MODEL PREDICTION
y_pred = model.predict(X_test)


