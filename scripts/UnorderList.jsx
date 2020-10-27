import React from 'react';
import Linkify from 'react-linkify';

export function UnorderList(prop) {
  function showImage(pic) {
    const startsWith = pic.toString().substr(0, 4);
    const endsWith = pic.toString().substr(-4);
    const spaces = pic.toString().indexOf(' ');

    if (spaces === -1 && startsWith === 'http' && (endsWith === '.png' || endsWith === '.jpg' || endsWith === '.gif')) {
      return true;
    }
    return false;
  }

  return (
    <ul className="chatRoom">
      {prop.msg.map((message, index) => (
        <li key={index} className="chatMessages">
          <p className={prop.name[index] === 'YodaBot' ? 'li_bot_user' : 'li_user'}>
            <img className="user_avatar" src={prop.pic[index]} alt="avatar" />
            {prop.name[index]}
            :
          </p>
          <p className={prop.name[index] === 'YodaBot' ? 'li_bot_message' : 'li_message'}>
            <Linkify>{message}</Linkify>
          </p>
          {showImage(prop.msg[index])
                        && <img className="sent_image" src={message} alt="display img" />}
        </li>
      ))}
    </ul>
  );
}
