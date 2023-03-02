import React from 'react'
import Chart from './Chart';

function ChartsList(props) {

    const items = props.charts.map(chart => (
        <Chart key={chart.id} id={chart.id} title={chart.title} data={chart.data} />
    ));

    return <ul>{items}</ul>;
}

export default ChartsList