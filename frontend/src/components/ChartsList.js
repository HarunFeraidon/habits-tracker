import React, { useState, useEffect } from 'react'
import Chart from './Chart';

function ChartsList(props) {

    const [items, setItems] = useState([])

    useEffect(() => {
        setItems(props.charts);
    }, [props.charts])

    function handleDelete(id) {
        console.log(id)
    }


    const itemsMap = items.map(chart => (
        <Chart key={chart.id} id={chart.id} title={chart.title} data={chart.data} handleDelete={handleDelete}/>
    ));


    return <ul>{itemsMap}</ul>;
}

export default ChartsList