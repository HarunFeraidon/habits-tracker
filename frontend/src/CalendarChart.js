import React from 'react'
import { ResponsiveCalendar } from '@nivo/calendar'

function CalendarChart(props) {
    // console.log(JSON.parse(props.data));
    // console.log(props.date_created);
    // console.log(props.one_year_ago);
    return (
        <div className='chart' style={{ height: 200 }}>
            {/* {props.data} */}
            {/* {props.date_created} */}
            {/* {typeof props.data} */}
            {/* {typeof JSON.parse(props.data)} */}
            <ResponsiveCalendar
                data={JSON.parse(props.data)}
                from={props.one_year_ago}
                to={props.date_created}
                emptyColor="#eeeeee"
                colors={['#61cdbb', '#97e3d5', '#e8c1a0', '#f47560']}
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