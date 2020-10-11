import * as React from "react";
import { Socket } from './Socket';


export function Form(props){

    const [text, setText] = React.useState(""); 
    // Current input being typed in the input box
  
    function handleChange(e) {
        setText(e.target.value);
        if (e.key === "Enter") {
            handleSubmit();
        }
    }
  
    function handleSubmit(e){
        e.preventDefault();
        Socket.emit('new message sent', {
            'message': text
        });
        setText("");
    }

    return(
        <form onSubmit={handleSubmit}>
            <input type="text" value={text} onChange={handleChange} />
            <button type="submit">Submit</button>
        </form>
    );
    
}