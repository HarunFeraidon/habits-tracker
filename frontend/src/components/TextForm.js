import React, { useState } from 'react';

function TextForm(props) {
    const [text, setText] = useState('');

    /**
     * updates text State that is rendered in the form
     * @param {object} event - key press on text field
     * @returns None
     */
    function handleChange(event) {
        setText(event.target.value);
    }

    /**
     * updates Chart by calling flask route to mark most recent day on Chart object complete
     * @param {int} id - id of specific Chart to update
     * @returns None
     */
    function handleSubmit(event, isSample) {
        event.preventDefault();
        console.log(props.submitFunction);
        console.log(`isSample: ${isSample}`);
        props.submitFunction(text, isSample);
    }

    return (
        <form>
            {/* <label htmlFor="text-input">Create a chart:</label> */}
            <input
                id="text-input"
                type="text"
                value={text}
                onChange={handleChange}
                placeholder="What is your new goal?"
            />
            <button
                className="btn btn-primary primary-button"
                type="submit"
                onClick={(event) => handleSubmit(event, false)}
            >
                Create Fresh Chart
            </button>
            <button
                className="btn btn-primary primary-button"
                type="submit"
                onClick={(event) => handleSubmit(event, true)}
            >
                Create Randomly Populated Chart
            </button>
        </form>
    );
}

export default TextForm