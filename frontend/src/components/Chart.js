import React, { useState } from 'react'
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
        <div className="row border">
            <div className="col-2 border">
                <div className="row border justify-content-around">
                    <div className="col-12 border">
                        <h3>{props.title}</h3>
                    </div>
                    <div className="col-12 border">
                        <button className='btn btn-primary'
                            onClick={() => handleUpdate(props.id)}> Complete today</button>
                    </div>
                    <div className="col-12 border">
                        <button className='btn btn-primary'
                            onClick={() => handleDelete(props.id)}> Delete Chart</button>
                    </div>
                </div>
            </div>
            <div className="col-10 border">
                <CalendarChart data={data} year_start={props.year_start} year_end={props.year_end} />
            </div>
        </div>
    )
}

export default Chart