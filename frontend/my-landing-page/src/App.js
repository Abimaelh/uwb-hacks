import { useState } from "react";
import './App.css';
var showResults = false;

function App() {
    const [formData, setFormData] = useState({
      message: ''
    });
    const[summaryData, setSummaryData] = useState({
      summMessage: '',
      source: ''
    });
    const[showResults, setShowResults] = useState(
      false
    )


    const handleChange = (event) => {
      const { name, value } = event.target;
      setFormData(prevFormData => ({
        ...prevFormData,
        [name]: value
      }));
    };
  
    const handleSubmit = (event) => {
      event.preventDefault();
      window.alert('Form Data Submitted:'+ formData.message);
      //back end placeholder logic here
      // Simple POST request with a JSON body using fetch
      const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: formData.message })
      };
      fetch("http://localhost:5000/submit", requestOptions)
          .then(response => response.json())
          .then(data => {
            setShowResults(true);
            setSummaryData({summMessage: data.summMessage, source: data.source})
          }
      ).catch(error => {console.log(error); window.alert(error)})

      //logic for converting the show results state
    };

    const handleGoBack = () => {
      setShowResults(false);
    }

  if(showResults) {
    return (
      <div>
      <p>{formData.message}</p>
      <p>{summaryData.summMessage}</p>
      <p>Sources</p>
      <button onClick={handleGoBack}>Go Back</button>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h2>POLISEE</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="message">Message</label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
            />
          </div>
          <button class="button" type="submit">Submit</button>

    </form>
      </header>
    </div>
  );

  
}

export default App;
