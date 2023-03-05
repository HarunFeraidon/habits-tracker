import './App.css';
import { useState, useEffect } from 'react';
import ChartsList from './components/ChartsList';
import TextForm from './components/TextForm';

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

  function handleCreate(title) {
    fetch(`/create/${title}`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(resp => resp.json())
      .then(resp => addNewChart(resp))
      .catch(error => {
        console.error('There was a problem with the API call:', error);
      });
  }

  function addNewChart(chart){
    console.log("Chart here: " + chart);
    let chartsCopy = [...charts];
    chartsCopy.push(chart)
    setCharts(chartsCopy);
  }

  return (
    <div className="App">
      <h2> Flask and React App</h2>
      <TextForm submitFunction={handleCreate} />
      <div className="items">
        <ChartsList charts={charts} />
      </div>
    </div>
  );
}

export default App;
