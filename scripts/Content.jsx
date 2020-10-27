import * as React from 'react';
import { Socket } from './Socket';
import { Form } from './Form';
import { UnorderList } from './UnorderList';
import { GoogleButton } from './GoogleButton';

export function Content() {
  const [message, addMessageToList] = React.useState([]);
  const [userName, addUsername] = React.useState([]);
  const [userImage, addUserImage] = React.useState([]);
  const [userCount, setUserCount] = React.useState(0);

  function sendMessage(data) {
    addMessageToList(data.allMessages);
    addUsername(data.user_of_message);
    addUserImage(data.users_avatar);
  }

  function updateUserCount() {
    React.useEffect(() => {
      Socket.on('usercount', (data) => {
        setUserCount(data.count);
      });
    });
  }

  function handleNewMessage() {
    React.useEffect(() => {
      Socket.on('new message received', sendMessage);
      return (() => {
        Socket.off('new message received', sendMessage);
      });
    });
  }

  handleNewMessage();
  updateUserCount();

  return (
    <div>
      <h1>
        User Count:
        {userCount}
      </h1>
      <div className="chat">
        <UnorderList msg={message} name={userName} pic={userImage} />
      </div>
      <div>
        <Form />
        <GoogleButton />
      </div>
    </div>
  );
}
