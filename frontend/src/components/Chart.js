import React, { useState, useEffect } from 'react'

function Chart(props) {

    const [data, setData] = useState(props.data)

    function handleClick(task, id) {
        let delete_or_finish = task == "delete" ? "DELETE" : "POST"
        fetch(`/${task}/${id}`, {
            method: delete_or_finish,
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(resp => resp.json())
            .then(resp => setData(resp.data))
            .catch(error => {
                console.error('There was a problem with the API call:', error);
            });
    }

    return (
        <div className="App">
            <p>{props.title}</p>
            <p>{data}</p>
            <div className='row'>
                <div className='col-md-1'>
                    <button className='btn btn-primary'
                        onClick={() => handleClick("finish", props.id)}> Complete today</button>
                    <button className='btn btn-primary'
                        onClick={() => handleClick("delete", props.id)}> Delete</button>
                </div>
            </div>

        </div>
    )
}

export default Chart