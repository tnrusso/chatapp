import * as React from "react";
import Linkify from 'react-linkify';

export function UnorderList(props) {
    
    function showImage(props){
        const startsWith = props.toString().substr(0,4);
        const endsWith = props.toString().substr(-4);
        const spaces = props.toString().indexOf(" ");
        
        if(spaces == -1 && startsWith == 'http' && (endsWith == '.png' || endsWith == '.jpg' || endsWith == '.gif')){
            return true;
        }else{
            return false;
        }
    }
    
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
                    {showImage(props.msg[index]) &&
                        <img className="sent_image" src={message}>
                        </img>
                    }
                </li>
            ))}
        </ul>
    );
}


