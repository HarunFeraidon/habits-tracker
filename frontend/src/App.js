import './App.css';
import { useState, useEffect } from 'react';
import ChartsList from './components/ChartsList';

function App() {

  const [charts, setCharts] = useState([])

  useEffect(() => {
    fetch('/listall', {
      'methods': 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(resp => resp.json())
      .then(resp => setCharts(resp))
      .catch(error => console.log(error))
  }, [])

  return (
    <div className="App">
      <h2> Flask and React App</h2>
      <div className="items">
        <ChartsList charts={charts} />
      </div>
    </div>
  );
}

export default App;
