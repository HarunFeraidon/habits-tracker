import './App.css';
import { useState, useEffect } from 'react';
import ChartsList from './components/ChartsList';
import TextForm from './components/TextForm';
import { GoogleLogin } from '@react-oauth/google';
import jwt_decode from "jwt-decode";
import { useJwt } from "react-jwt";


function App() {

  const [charts, setCharts] = useState([]);

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

  const [authToken, setAuthToken] = useState("");

  const responseMessage = (credentialResponse) => {
    var decoded = jwt_decode(credentialResponse.credential);
    console.log(decoded);
    createUser(decoded.email)
  };
  const errorMessage = (error) => {
    console.log(error);
  };

  // let authToken = '';

  function createUser(email) {
    const formData = new FormData()
    formData.append('email', email)

    fetch('/create_user', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        console.log(typeof(data));
        console.log("data.token: " + data.token)
        // authToken = data.token;
        setAuthToken(data.token)
        localStorage.setItem('authToken', authToken);
      })
      .catch(error => {
        console.error(error)
      })
  }

  function printToken(){
    console.log(authToken)
  }

  function fetchAuthenticatedData() {
    // Use the authToken in the headers of authenticated requests
    fetch('/api/protected', {
      headers: {
        'Authorization': `${authToken}` // Use the stored authToken
      }
    })
    .then(response => {
      response.json()
    })
    .then(response => {
      console.log(response)
    })
    .catch(error => {
      console.error(error);
    });
  }

  return (
    <div className="App">
      <GoogleLogin
        onSuccess={responseMessage}
        onError={errorMessage}
      />;
      <button onClick={printToken}>Click here</button>
      <button onClick={fetchAuthenticatedData}>authenticated_route here</button>
      {/* <div className="container text-center">
        <div className="row justify-content-md-center">
          
          <h4>Track Your Goals</h4>
        </div>
        <div className="row ">
          <TextForm submitFunction={handleCreate} />
        </div>
      </div>
      <div className="container text-center">
        <ChartsList charts={charts} handleDelete={handleDelete} />
      </div> */}
      {/* Conditionally render content based on authToken */}
      {authToken ? (
        <div className="container text-center">
          <div className="row justify-content-md-center">
            <h4>Track Your Goals</h4>
          </div>
          <div className="row ">
            {/* Render TextForm component */}
            <TextForm submitFunction={handleCreate} />
          </div>
        </div>
      ) : null}

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
