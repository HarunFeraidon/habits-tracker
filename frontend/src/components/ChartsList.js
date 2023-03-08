import React, { useState, useEffect } from 'react'
import Chart from './Chart';

function ChartsList(props) {

    const [items, setItems] = useState([])

    useEffect(() => {
        setItems(props.charts);
    }, [props.charts])

    function handleDelete(id) {
        fetch(`/delete/${id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(resp => resp.json())
            .then(resp => refreshItems(resp, id))
            .catch(error => {
                console.error('There was a problem with the API call:', error);
            });
    }

    function refreshItems(resp, id){
        if(resp.status === 204){
            const newItems = items.filter((item) => item.id !== id);
            setItems(newItems);
        }
    }


    const itemsMap = items.map(chart => (
        <Chart key={chart.id} id={chart.id} title={chart.title} data={chart.data}
        year_start={chart.year_start} year_end={chart.year_end} handleDelete={handleDelete}/>
    ));


    return <ul>{itemsMap}</ul>;
}

export default ChartsList