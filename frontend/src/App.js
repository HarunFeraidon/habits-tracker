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

  function handleCreate(){
    console.log(43);
  }

  return (
    <div className="App">
      <h2> Flask and React App</h2>
      <div className="items">
        <button className='btn btn-primary'
        onClick={() => handleCreate()}>Create Chart</button>
        <ChartsList charts={charts} />
      </div>
    </div>
  );
}

export default App;
