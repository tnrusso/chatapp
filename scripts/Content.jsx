import React, { useState } from "react";
import { Socket } from './Socket';

export function Content(props) {
  // List of messages that are saved
  const [message, addMessageToList] = useState([]);
  
  function handleNewMessage(newMsg) {
    addMessageToList(prevList => {
      return [...prevList, newMsg];
    });
  }

  return (
    <div>
      <div className="chat" id="chat">
        <Messages val={message} />
      </div>
      <div className="submission">
        <Form onNewMessage={handleNewMessage}/> 
      </div>
    </div>
  );
}

// Form holds input text box, submit button
function Form(props){
  // text holds the current input being typed in the input box
  const [text, setText] = useState("");
  
  // to submit message if the user types enter
  function handleChange(e) {
    setText(e.target.value);
    if (e.key === "Enter") { 
      handleSubmit();
    }
  }
  
  // Set props.onNewMessage to the input text. This will send the text input back to Content(), which will call handleNewMessage() to add it to the list of messages
  function handleSubmit(e){
    e.preventDefault();
    props.onNewMessage(text); 
    setText("");
  }

  return(
    <form onSubmit={handleSubmit}>
      <input type="text" value={text} onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>);
}

// props.val is the state for the list of messages. 
function Messages(props) {
  return (
    <ul className="chatRoom">
      {props.val.map((message, index) => (
        <li key={index} className="chatMessages">{message}</li>
      ))}
    </ul>
  );
}