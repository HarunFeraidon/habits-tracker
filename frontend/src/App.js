import './App.css';
import { useState, useEffect } from 'react';

function App() {

  const [charts, setCharts] = useState([])

  useEffect( () => {
    fetch('http://127.0.0.1:5000/get/2', {
      'methods': 'GET',
      headers: {
        'Content-Type':'application/json'
      }
    })
    .then(resp => resp.json())
    .then(resp => console.log(resp))
    .catch(error => console.log(error))
  })

  return (
    <div className="App">
      <h2> flask and react app</h2>
    </div>
  );
}

export default App;
