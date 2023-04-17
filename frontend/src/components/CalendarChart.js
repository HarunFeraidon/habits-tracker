import React from 'react'
import { ResponsiveCalendar } from '@nivo/calendar'

function CalendarChart(props) {
    const date_object_start = new Date(Date.parse(props.year_start));
    const year_start = date_object_start.getFullYear();
    const from_date = new Date(year_start + 1, 0, 1); // very weird behavior, had to year+1 because of how Date.parse works
    const date_object_end = new Date(Date.parse(props.year_end));
    const year_end = date_object_end.getFullYear();
    const to_date = new Date(year_end, 11, 31);

    const colors = [
        "#f47560",
        "#61cdbb",
    ];

    const ticks = ["Loss", 0, 1000];
    const colorScaleFn = (value) => {
        if (value === 0) {
            return colors[0];
        }
        if (value === 1) {
            return colors[1];
        }
        return colors[colors.length - 1];
    };

    colorScaleFn.ticks = () => ticks;

    return (
        <div className='chart' style={{ height: 200 }}>
            <ResponsiveCalendar
                data={JSON.parse(props.data)}
                from={from_date}
                to={to_date}
                emptyColor="#eeeeee"
                colors={['#f47560', '#97e3d5', '#e8c1a0', '#61cdbb']}
                colorScale={colorScaleFn}
                margin={{ top: 40, right: 40, bottom: 40, left: 40 }}
                yearSpacing={40}
                monthBorderColor="#ffffff"
                dayBorderWidth={2}
                dayBorderColor="#ffffff"
                legends={[
                    {
                        anchor: 'bottom-right',
                        direction: 'row',
                        translateY: 36,
                        itemCount: 4,
                        itemWidth: 42,
                        itemHeight: 36,
                        itemsSpacing: 14,
                        itemDirection: 'right-to-left'
                    }
                ]}
            />
        </div>
    )
}

export default CalendarChart