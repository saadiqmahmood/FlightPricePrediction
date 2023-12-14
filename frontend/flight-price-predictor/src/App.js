import React, { useState, useRef } from 'react';
import './App.css';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

function App() {
  // State to store form data
  // This state holds the values entered in the form, such as airline, city, etc.
  const [formData, setFormData] = useState({
    airline: '',
    source_city: '',
    departure_time: '',
    stops: '',
    destination_city: '',
    class: '',
    days_left: ''
  });

  // State to store the prediction result
  // This state will hold the predicted flight price after the form is submitted.
  const [prediction, setPrediction] = useState(null);

  // Ref for the result container
  // This reference is used to scroll to the prediction result section after prediction.
  const resultRef = useRef(null); 

  // Ref for the "Flight Price Predictor" section
  // This reference is used to scroll to the form section when the user clicks "Get Started".
  const predictorRef = useRef(null);

  // Function to handle click on "Get Started" button
  const scrollToPredictor = () => {
    // Scrolls smoothly to the "Flight Price Predictor" section referenced by predictorRef
    // This makes the user experience more intuitive and interactive.
    predictorRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };


  const [startDate, setStartDate] = useState(null);

  // Define the minimum and maximum dates for the date picker
  const minDate = new Date(); // Initialize to today's date
  minDate.setDate(minDate.getDate() + 1); // Set the minimum date to tomorrow
  
  const maxDate = new Date(minDate); // Start from the minimum date (tomorrow)
  maxDate.setDate(maxDate.getDate() + 49); // Set the maximum date to 50 days from the minimum date
  
  // Function to calculate the number of days left until the selected date
  const calculateDaysLeft = (selectedDate) => {
    const oneDay = 24 * 60 * 60 * 1000; // Milliseconds in one day
  
    // Reset the time part to midnight for both dates for accurate day calculation
    const selectedDateMidnight = new Date(selectedDate.setHours(0, 0, 0, 0));
    const minDateMidnight = new Date(minDate.setHours(0, 0, 0, 0));
  
    // Calculate the difference in days between the selected date and the minimum date
    const daysLeft = Math.ceil((selectedDateMidnight - minDateMidnight) / oneDay) + 1;
    // Ensure the calculated days_left is within the 1 to 50 range
    return daysLeft >= 1 && daysLeft <= 50 ? daysLeft : null;
  };  

  /// Handle date change from DatePicker
  const handleDateChange = (date) => {
    // Update the startDate state with the new date selected by the user
    setStartDate(date);

    // Calculate the number of days left until the selected date
    const daysLeft = calculateDaysLeft(date);

    // Log the selected date and the calculated days left for debugging purposes
    console.log(`Selected Date: ${date}, Days Left: ${daysLeft}`);

    // Update the formData state, specifically the days_left field
    // This ensures that the form data reflects the latest date selection
    setFormData({
      ...formData,
      days_left: daysLeft // Update days_left in formData    
    }); 
  };


  /// Handle form input changes
  const handleChange = (e) => {
    // Create an updated version of the formData state
    // This includes the current state and the new value for the changed field
    const updatedFormData = {
      ...formData,
      [e.target.name]: e.target.value
    };

    // Log the name of the field that changed and its new value for debugging
    console.log(`Field changed: ${e.target.name}, New Value: ${e.target.value}`);

    // Update the formData state with the new values
    setFormData(updatedFormData);
  };



  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission behavior
    setPrediction(null); // Reset the prediction state before making a new prediction

    try {
      // Send a POST request to the prediction API endpoint
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData), // Send the form data as JSON
      });
      const result = await response.json(); // Parse the JSON response

      // Round the prediction to the nearest whole number
      const roundedPrediction = Math.round(result.prediction);

      // Update the prediction state with the rounded prediction
      setPrediction(roundedPrediction);

      // Scroll smoothly to the result section for better user experience
      resultRef.current.scrollIntoView({ behavior: 'smooth' });

      // Additional code to handle the prediction result can be added here
    } catch (error) {
      // Log any errors that occur during the fetch operation
      console.error('Error:', error);
    }
  };

  return (
    <div className='App'>
      <div className='App-header'>
        <header>
            <h1>SkySavvy.io</h1>
            <button onClick={scrollToPredictor}>
              Get Started
            </button>
        </header>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#EFFAFD" fill-opacity="1" d="M0,32L60,58.7C120,85,240,139,360,133.3C480,128,600,64,720,48C840,32,960,64,1080,96C1200,128,1320,160,1380,176L1440,192L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"></path></svg>
      </div>
      <div className='App-info'>
        <div className='App-welcome'>
          <h1>
            Welcome to SkySavvy: Navigating India's Airspace with Ease
          </h1>
          <p>
            SkySavvy is thrilled to introduce you to a specialised flight prediction experience
            for India's top metro cities: Delhi, Mumbai, Bangalore, Kolkata, Hyderabad, and
            Chennai. Our app is tailored to offer insightful predictions for flights spanning
            up to 50 days from the present day.
          </p>
        </div>
        <div className='App-scope'>
          <h1>
            Current Scope & The Path Ahead
          </h1>
          <p>
            As SkySavvy is currently in its prototype phase, our predictions are based on a select
            yet robust dataset. This prototype version enables you to explore potential flight 
            options within a 50-day window. We see this as our first leap towards providing a broader 
            and more in-depth flight prediction service.
          </p>
          <p>
            Our team is actively working to enrich our data and refine our predictive algorithms. Your journey
            with SkySavvy today lays the foundation for a more expansive tomorrow.
          </p>
        </div>
        <div className='App-next'>
          <h1>
            Your Next Step: Explore Our Flight Predictor
          </h1>
          <p>
            Ready to plan your journey? Head over to our Flight Predictor section. Here, you can input your travel
            details and discover the best upcoming flight options for your travel needs between India's top cities
          </p>
        </div>
      </div>
      <div className='App-predictor-title'>
        <div className='' ref={predictorRef}>
          <h1>
            Flight Price Predictor
          </h1>
        </div>
      </div>
      <div className='form-container'>
        <form onSubmit={handleSubmit}>
          <div className='form-group'>
            <select id='airline' name="airline" value={formData.airline} onChange={handleChange}>
              <option value="">Airline</option>
              <option value="AirAsia">AirAsia</option>
              <option value="Vistara">Vistara</option>
              <option value="Air_India">Air_India</option>
              <option value="Indigo">Indigo</option>
              <option value="GO_FIRST">GO_FIRST</option>
              <option value="SpiceJet">SpiceJet</option>
            </select>
          </div>
        
          <div className='form-group'>
            <select id="source_city" name="source_city" value={formData.source_city} onChange={handleChange}>
              <option value="">Source City</option>
              <option value="Delhi">Delhi</option>
              <option value="Mumbai">Mumbai</option>
              <option value="Hyderabad">Hyderabad</option>
              <option value="Kolkata">Kolkata</option>
              <option value="Bangalore">Bangalore</option>
              <option value="Chennai">Chennai</option>
            </select>
          </div>          

          <div className='form-group'>
            <select id="destination_city" name="destination_city" value={formData.destination_city} onChange={handleChange}>
              <option value="">Where to?</option>
              <option value="Delhi">Delhi</option>
              <option value="Mumbai">Mumbai</option>
              <option value="Hyderabad">Hyderabad</option>
              <option value="Kolkata">Kolkata</option>
              <option value="Bangalore">Bangalore</option>
              <option value="Chennai">Chennai</option>
            </select>
          </div>

          <div className='form-group'>
            <DatePicker
              selected={startDate}
              onChange={handleDateChange} // Updated to use handleDateChange
              dateFormat="dd/MM/yyyy"
              minDate={minDate}
              maxDate={maxDate}
              placeholderText="Departure Date"
              className="form-control"
            />
          </div>


          <div className='form-group'>
            <select id="departure_time" name="departure_time" value={formData.departure_time} onChange={handleChange}>
              <option value="Late_Night">00:00</option>
              <option value="Early_Morning">05:00</option>
              <option value="Morning">08:00</option>
              <option value="Afternoon">12:00</option>
              <option value="Evening">18:00</option>
              <option value="Night">21:00</option>
            </select>
          </div>

          <div className='form-group'>
            <select id="stops" name="stops" value={formData.stops} onChange={handleChange}>
              <option value="">Stops</option>
              <option value="zero">Zero</option>
              <option value="one">One</option>
              <option value="two_or_more">Two or More</option>
            </select>
          </div>

          <div className='form-group'>
            <select id="class" name="class" value={formData.class} onChange={handleChange}>
              <option value="">Class</option>
              <option value="Economy">Economy</option>
              <option value="Business">Business</option>
            </select>
          </div>

          <div className='form-group'>
            <button type="submit">Predict</button>
          </div>

        </form>
      </div>
      <div className='App-result'>
        {/* Reference to the result container for scrolling */}
        <div ref={resultRef}>
          {/* Conditional rendering: Display the prediction result if it's not null */}
          {prediction !== null && (
            <h1>
              Predicted Price: ${prediction}
            </h1>
          )}
        </div>
      </div>
      <div className='App-closing'>
        <div className=''>
          <p>
            Your insights and feedback are invaluable as we strive to enhance SkySavvy. 
            Share your thoughts, and let's shape the future of travel together!
          </p>
          <p>
            Thank You for Being Part of Our First Flight!
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
