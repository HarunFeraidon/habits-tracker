import './App.css';
import { useState, useEffect } from 'react';
import ChartsList from './components/ChartsList';
import TextForm from './components/TextForm';
import { GoogleLogin } from '@react-oauth/google';
import jwt_decode from "jwt-decode";


function App() {

  const [charts, setCharts] = useState([]);
  const [authToken, setAuthToken] = useState("");

  const fetchDataWithAuthToken = (authToken) => {
    fetch('/listall', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${authToken}` // Use the stored authToken
      }
    })
      .then(resp => resp.json())
      .then(resp => setCharts(resp))
      .catch(error => console.log(error));
  };

  // Call the function with the authToken when it's ready, e.g., in a useEffect hook
  useEffect(() => {
    // Check if authToken is ready (e.g., fetched, received from server, etc.)
    if (authToken) {
      fetchDataWithAuthToken(authToken);
    }
  }, [authToken]); // Update the effect whenever the authToken changes

  function handleCreate(title) {
    fetch(`/create/${title}`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${authToken}` // Use the stored authToken
      }
    })
      .then(resp => resp.json())
      .then(resp => addNewChart(resp))
      .catch(error => {
        console.error('There was a problem with the API call:', error);
      });
  }

  function addNewChart(chart) {
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

  const responseMessage = (credentialResponse) => {
    var decoded = jwt_decode(credentialResponse.credential);
    createUser(decoded.email)
  };
  const errorMessage = (error) => {
    console.log(error);
  };

  function createUser(email) {
    const formData = new FormData()
    formData.append('email', email)

    fetch('/create_user', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        setAuthToken(data.token)
      })
      .catch(error => {
        console.error(error)
      })
  }

  function handleLogout(){
    setAuthToken("") // resets authToken
  }

  return (
    <div className="App">

      {authToken ? (
        <div className="container text-center">
          <div className="row justify-content-md-center">
            <h4>Track Your Goals</h4>
          </div>
          <button onClick={handleLogout}>Sign out</button>
          <div className="row ">
            {/* Render TextForm component */}
            <TextForm submitFunction={handleCreate} />
          </div>
        </div>
      ) : (
          <div class="container">
            <h3 class="text-center">Welcome to your daily Habits Tracker</h3>
            <p class="text-center welcome">To get started, authenticate through your Google account.</p>
            <p class="text-center subtle-text welcome">Don't worry, the only information used is your email account, to create yourself a unique account</p>
            <GoogleLogin
              onSuccess={responseMessage}
              onError={errorMessage}
            />
          </div>
      )}

      {/* Conditionally render content based on authToken */}
      {authToken ? (
        <div className="container text-center">
          {/* Render ChartsList component */}
          <ChartsList charts={charts} handleDelete={handleDelete} />
        </div>
      ) : null}
    </div>
  );
}

export default App;
