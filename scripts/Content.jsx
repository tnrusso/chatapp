import * as React from "react";
import { Socket } from './Socket';

export function Content(props) {
  // List of messages that are saved
  const [message, addMessageToList] = React.useState([]);
  const [userN, addUser] = React.useState([]);
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
    addUser(data['user_of_message']);
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
        <Messages msg={message} un={userN} />
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



// props.msg is the state for the list of messages. 
function Messages(props) {
  return (
    <ul className="chatRoom">
      {props.msg.map((message, index) => (
        <li key={index} className="chatMessages">
          <p className={props.un[index]=='YodaBot' ? "li_bot_user" : "li_user"}>{props.un[index]}: </p>
          <p className={props.un[index]=='YodaBot' ? "li_bot_message" : "li_message"}>
            <img className={props.un[index]=='YodaBot' ? 'yodaImg' : 'noImg'}></img>
            {message}
          </p>
        </li>
      ))}
    </ul>
  );
}