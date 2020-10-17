import * as React from "react";
import { Content } from './Content';
import Linkify from 'react-linkify';

export function UnorderList(props) {
    
    return (
        <ul className="chatRoom">
            {props.msg.map((message, index) => (
                <li key={index} className="chatMessages">
                    <p className={props.name[index]=='YodaBot' ? "li_bot_user" : "li_user"}>
                        <img className="user_avatar" src={props.pic[index]}></img>
                        {props.name[index]}: 
                    </p>
                    <p className={props.name[index]=='YodaBot' ? "li_bot_message" : "li_message"}>
                        <Linkify>{message}</Linkify>
                    </p>
                </li>
            ))}
        </ul>
    );
}