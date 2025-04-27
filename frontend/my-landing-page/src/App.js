import logo from './logo.svg';
import './App.css';
import {useState} from "react";
import Button from './components/Button';
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
      //back end placeholder logic here
      // Simple POST request with a JSON body using fetch
      const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: 'React POST Request Example' })
      };
      fetch('https://reqres.in/api/posts', requestOptions)
          .then(response => response.json())
          .then(data => {
            setShowResults(true);
            setSummaryData({summMessage: "this is not ai", source: "big brain"})
          });

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
