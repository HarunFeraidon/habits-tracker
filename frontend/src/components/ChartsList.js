import React from 'react'

function ChartsList(props) {

    function handleClick(task, id) {
        let delete_or_finish = task == "delete" ? "DELETE" : "POST"
        fetch(`/${task}/${id}`, {
            method: delete_or_finish,
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
            })
            .catch(error => {
                console.error('There was a problem with the API call:', error);
            });
    }

    return (
        <div className="App">
            {props.charts && props.charts.map(chart => {
                return (
                    <div key={chart.id}>
                        <p>{chart.title}</p>
                        <p>{chart.data}</p>
                        <div className='row'>
                            <div className='col-md-1'>
                                <button className='btn btn-primary'
                                    onClick={() => handleClick("finish", chart.id)}> Complete today</button>
                                <button className='btn btn-primary'
                                    onClick={() => handleClick("delete", chart.id)}> Delete</button>
                            </div>
                        </div>
                    </div>
                )
            })}
        </div>
    );
}

export default ChartsList