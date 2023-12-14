import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os


class CustomLabelEncoder:
    def __init__(self):
        self.label_map = {}


    def fit(self, data):
        unique_labels = set(data)
        self.label_map = {label: idx for idx, label in enumerate(unique_labels)}
        self.label_map['unknown'] = len(unique_labels)  # Handle unknown labels


    def transform(self, data):
        return [self.label_map.get(label, self.label_map['unknown']) for label in data]


    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)


# Set the working directory to the root of your project
os.chdir('C:/Users/Saadiq Mahmood/OneDrive/UA92/FlightPricePrediction')


# Initialise Flask application
# This creates an instance of the Flask class which will be our WSGI application.
app = Flask(__name__)


# Enable CORS for all routes
# CORS (Cross-Origin Resource Sharing) is enabled for the '/predict' route.
# This allows the frontend running on 'http://localhost:3000' to interact with the Flask app.
CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}})


@app.before_request
def load_encoders():
    global encoder_mappings, scaler, label_encoders, model
    # Load the label encoder mappings, scaler, and the pre-trained model
    # This ensures that these components are available globally and can be used in the prediction endpoint
    encoder_mappings = joblib.load('backend/label_encoder_mappings.pkl')  # Load mappings for label encoders
    scaler = joblib.load('backend/min_max_scaler.pkl')  # Load the MinMaxScaler for numerical features
    label_encoders = joblib.load('backend/label_encoder.pkl')  # Load the label encoders for categorical features
    model = joblib.load('backend/random_forest_model.pkl')  # Load the pre-trained Random Forest model


@app.route('/predict', methods=['POST'])
def predict():
    # Get data from POST request
    # This data is expected to be in JSON format containing the features required for prediction
    data = request.json
    print("Received data:", data)  # Log the received data for debugging


    # Convert the incoming JSON data to a pandas DataFrame
    # This is necessary as the model expects input in this format
    processed_data = pd.DataFrame([data])
    print("Initial processed data:", processed_data)  # Log the initial processed data


    # Apply label encoders to categorical features
    # This step converts categorical features into a format that the model can understand
    categorical_features = ['airline', 'source_city', 'departure_time', 'stops', 'destination_city', 'class']
    for feature in categorical_features:
        if feature in processed_data:
            processed_data[feature] = label_encoders[feature].transform(processed_data[feature])
   
    # Apply scaler to numerical features
    # Scaling ensures that numerical features are in the same range as during model training
    numerical_features = ['days_left']  # Example feature
    if 'days_left' in processed_data:
        processed_data[numerical_features] = scaler.transform(processed_data[numerical_features])


    print("Processed data for prediction:", processed_data)  # Log the processed data


    # Make prediction using the pre-trained model
    try:
        prediction = model.predict(processed_data)
        print("Prediction:", prediction, "\n")  # Log the prediction
        # Return the prediction in a JSON format
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        # Log any errors that occur during prediction
        print("Error during prediction:", e,"\n")
        # Return an error message and a 500 internal server error status
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application


