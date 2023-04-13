import React, { useState } from 'react';

function TextForm(props) {
    const [text, setText] = useState('');

    function handleChange(event) {
        setText(event.target.value);
    }

    function handleSubmit(event) {
        event.preventDefault();
        console.log(`Text submitted: ${text}`);
        props.submitFunction(text);
    }

    function handleSampleSubmit(event) {
        event.preventDefault();
        console.log(`Text submitted: ${text}`);
        props.sampleSubmitFunction(text);
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
                onClick={handleSubmit}
            >
                Create Fresh Chart
            </button>
            <button
                className="btn btn-primary primary-button"
                type="submit"
                onClick={handleSampleSubmit}
            >
                Create Randomly Populated Chart
            </button>
        </form>
    );
}

export default TextForm