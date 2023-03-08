import React, { useState, useEffect } from 'react'
import CalendarChart from './CalendarChart';

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

    function handleDelete(id) {
        props.handleDelete(id)
    }

    return (
        <div className="item">
            <CalendarChart data={data} year_start={props.year_start} year_end={props.year_end}/>
            <div className='row'>
                <div className='col-md-1'>
                    <button className='btn btn-primary'
                        onClick={() => handleUpdate(props.id)}> Complete today</button>
                    <button className='btn btn-primary'
                        onClick={() => handleDelete(props.id)}> Delete Chart</button>
                </div>
            </div>

            <hr />

        </div>
    )
}

export default Chart