import * as React from "react";
import { Socket } from './Socket';

export function Content(props) {
  // List of messages that are saved
  const [message, addMessageToList] = React.useState([]);
  const [userCount, setUserCount] = React.useState(0);
  
  function handleNewMessage() {
    React.useEffect(() => {
      Socket.on('new message received', sendMessage);
      return(() => {
        Socket.off('new message received', sendMessage);
      });
    });
  }
  
  function sendMessage(data){
    addMessageToList(data['allMessages']);
  }
  
  function updateUserCount(){
      React.useEffect(() => {
      Socket.on('usercount', (data) => { 
        setUserCount(data['count']);
      });
    });
  }
  
  handleNewMessage();
  updateUserCount();

  return (
    <div>
      <h1>User Count: {userCount}</h1>
      <div className="chat" id="chat">
        <Messages val={message} />
      </div>
      <div className="submission">
        <Form/> 
      </div>
    </div>
  );
}



// Form holds input text box, submit button
function Form(props){
  // text holds the current input being typed in the input box
  const [text, setText] = React.useState("");
  
  // to submit message if the user types enter
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