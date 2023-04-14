import React, { useState } from 'react'
import CalendarChart from './CalendarChart';

function Chart(props) {

    const [data, setData] = useState(props.data)

    /**
     * updates Chart by calling flask route to mark most recent day on Chart object complete
     * @param {int} id - id of specific Chart to update
     * @returns None
     */
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
        <div className="row">
            <div className="col-2">
                <div className="row justify-content-around">
                    <div className="col-12">
                        <h3>{props.title}</h3>
                    </div>
                    <div className="col-12">
                        <button className='btn btn-primary primary-button'
                            onClick={() => handleUpdate(props.id)}> Complete today</button>
                    </div>
                    <div className="col-12">
                        <button className='btn btn-primary primary-button'
                            onClick={() => handleDelete(props.id)}> Delete Chart</button>
                    </div>
                </div>
            </div>
            <div className="col-10">
                <CalendarChart data={data} year_start={props.year_start} year_end={props.year_end} />
            </div>
        </div>
    )
}

export default Chart