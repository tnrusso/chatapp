import * as React from "react";
import { Content } from './Content';


export function UnorderList(props) {
    
    return (
        <ul className="chatRoom">
            {props.msg.map((message, index) => (
                <li key={index} className="chatMessages">
                    <p className={props.name[index]=='YodaBot' ? "li_bot_user" : "li_user"}>{props.name[index]}: </p>
                    <p className={props.name[index]=='YodaBot' ? "li_bot_message" : "li_message"}>
                        <img className={props.name[index]=='YodaBot' ? 'yodaImg' : 'noImg'}></img>
                        {message}
                    </p>
                </li>
            ))}
        </ul>
    );
}