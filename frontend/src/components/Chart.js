import React, { useState, useEffect } from 'react'

function Chart(props) {

    const [data, setData] = useState(props.data)

    function handleUpdate(id) {
        fetch(`/finish/${id}`, {
            method: "POST",
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
        <div className="item">
            <p>{props.title}</p>
            <p>{data}</p>
            <div className='row'>
                <div className='col-md-1'>
                    <button className='btn btn-primary'
                        onClick={() => handleUpdate(props.id)}> Complete today</button>
                </div>
            </div>

            <hr />

        </div>
    )
}

export default Chart