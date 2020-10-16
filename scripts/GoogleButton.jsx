import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';

export function GoogleButton(){
    
    function handleLogin(response){
        const fullname = response.profileObj.name;
        const emailAdress = response.profileObj.email;
        const avatarLink = response.profileObj.imageUrl;
        Socket.emit('new google user', {
            'name': fullname,
            'email': emailAdress,
            'avatar': avatarLink
        });
    }
    
    return(
        <GoogleLogin
            clientId="477035920625-38n6lbf1m04mtpsfnvsiogmp4dlin790.apps.googleusercontent.com"
            buttonText="Sign in with Google"
            onSuccess={handleLogin}
            inSignedIn={true}
            cookiePolicy={'single_host_origin'}
        />    
    );
}