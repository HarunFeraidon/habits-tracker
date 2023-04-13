import React, { useState } from 'react';

function TextForm(props) {
    const [text, setText] = useState('');

    function handleChange(event) {
        setText(event.target.value);
    }

    function handleSubmit(event, isSample) {
        event.preventDefault();
        if (isSample) {
            props.sampleSubmitFunction(text);
        } else {
            props.submitFunction(text);
        }
    }

    return (
        <form>
            <label htmlFor="text-input">Create a chart:</label>
            <input
                id="text-input"
                type="text"
                value={text}
                onChange={handleChange}
                placeholder="What is your goal?"
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