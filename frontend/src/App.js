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

  function addNewChart(chart) {
    console.log("Chart here: " + chart);
    let chartsCopy = [...charts];
    chartsCopy.push(chart)
    setCharts(chartsCopy);
  }

  return (
    <div className="App">
      <div class="container text-center">
        <div class="row justify-content-md-center">
          <h4>Track Your Goals</h4>
        </div>
        <div class="row ">
          <TextForm submitFunction={handleCreate} />
        </div>
      </div>
      <div className="container text-center">
        <ChartsList charts={charts} />
      </div>
    </div>
  );
}

export default App;
