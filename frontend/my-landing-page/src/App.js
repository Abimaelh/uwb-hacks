import logo from './logo.svg';
import './App.css';
import {useState} from "react";
var showResults = false;

function App() {
    const [formData, setFormData] = useState({
      message: ''
    });
    const[summaryData, setSummaryData] = useState({
      summMessage: '',
      source: ''
    });
  
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
      //logic for converting the show results state
    };

  if(showResults) {
    return (
      <div className="App">
      <p>{formData.message}</p>
      <p>{summaryData.summMessage}</p>
      <p>Sources</p>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h2>POLISEE</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="message">Message:</label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
            />
          </div>
          <button type="submit">Submit</button>

    </form>
      </header>
    </div>
  );

  
}

export default App;
