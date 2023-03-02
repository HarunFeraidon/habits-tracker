import React, { useState, useEffect } from 'react'
import Chart from './Chart';

function ChartsList(props) {

    const [items, setItems] = useState(initItems(props.charts))

    function initItems(charts) {
        console.log("charts")
        console.log(charts)
        let result = charts.map(chart => (
            <Chart key={chart.id} id={chart.id} title={chart.title} data={chart.data} />
        ))
        console.log("result")
        console.log(result)
        return result;
    }

    function handleClick(id) {
        fetch(`/delete/${id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(resp => resp.json())
            .then(resp => console.log(resp))
            .catch(error => {
                console.error('There was a problem with the API call:', error);
            });
    }

    return (
        <div>
            <ul>{items.length}</ul>
            <button className='btn btn-primary'
                onClick={() => handleClick(props.id)}>Delete</button>
        </div>
    );
}

export default ChartsList