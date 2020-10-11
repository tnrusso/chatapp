import * as React from "react";
import { Socket } from './Socket';
import { Form } from './Form';
import { UnorderList } from './UnorderList';


export function Content(props) {
    const [message, addMessageToList] = React.useState([]);
    const [userName, addUsername] = React.useState([]);
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
        addUsername(data['user_of_message']);
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
            <div className="chat">
                <UnorderList msg={message} name={userName} />
            </div>
            <div>
                <Form/> 
            </div>
        </div>
    );
  
}

