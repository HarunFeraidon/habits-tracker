import './App.css';
import { useState, useEffect } from 'react';
import ChartsList from './components/ChartsList';
import TextForm from './components/TextForm';
import Axios from "axios";

function App() {

  const [charts, setCharts] = useState([]);
  const [user, setUser] = useState({});
  const [status, setStatus] = useState(false);
  const [loginButton, setLoginButton] = useState(null);

  useEffect(() => {
    fetch('/userinfo')
      .then(resp => resp.json())
      .then(resp => {
        setUser(resp)
        setStatus(resp["authenticated"])
        if (status == false) {
          setLoginButton(
            <a href="#" onClick={() => handleLogin()}>log in here</a>
            // <button className='btn btn-primary'
            //   onClick={() => handleLogin()}> Login with Google</button>
          );
        }
        else {
          setLoginButton(
            <button className='btn btn-primary'
              onClick={() => handleLogout()}> Logout</button>
          );
        }
        console.log(resp["authenticated"])
      })
      .catch(error => console.log(error))
  }, [])

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

  function handleDelete(id) {
    fetch(`/delete/${id}`, {
      method: "DELETE",
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(resp => resp.json())
      .then(resp => {
        if (resp.status === 204) {
          const newCharts = charts.filter((chart) => chart.id !== id);
          setCharts(newCharts);
        }
      })
      .catch(error => {
        console.error('There was a problem with the API call:', error);
      });
  }

  function handleLogin() {
    console.log("login")
    fetch('/login')
      .then(response => response.json())
      .then(data => {
        // Redirect to authorization page
        window.location.href = data.auth_url;
      })
      .catch(error => {
        // Handle error
      });

  }

  function handleLogout() {
    console.log("logout")
  }

  return (
    <div className="App">
      <div className="container text-center">
        <div className="row justify-content-md-center">
          {loginButton}
          <h4>Track Your Goals</h4>
        </div>
        <div className="row ">
          <TextForm submitFunction={handleCreate} />
        </div>
      </div>
      <div className="container text-center">
        <ChartsList charts={charts} handleDelete={handleDelete} />
      </div>
    </div>
  );
}

export default App;
