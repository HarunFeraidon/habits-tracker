import React, { useState, useEffect } from 'react'
import Chart from './Chart';

function ChartsList(props) {

    const [items, setItems] = useState([])

    useEffect(() => {
        setItems(props.charts);
    }, [props.charts])

    function handleDelete(id){
        props.handleDelete(id);
    }

    return <ul>{items.map(chart => (
        <Chart key={chart.id} id={chart.id} title={chart.title} data={chart.data}
            year_start={chart.year_start} year_end={chart.year_end} handleDelete={handleDelete} />
    ))}</ul>;
}

export default ChartsList