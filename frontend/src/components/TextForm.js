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

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="text-input">Enter some text:</label>
            <input
                id="text-input"
                type="text"
                value={text}
                onChange={handleChange}
            />
            <button className='btn btn-primary' type="submit">Submit</button>
            {/* <p>You entered: {text}</p> */}
        </form>
    );
}

export default TextForm