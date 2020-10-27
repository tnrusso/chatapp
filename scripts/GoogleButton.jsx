import * as React from 'react';
import GoogleLogin from 'react-google-login';
import { Socket } from './Socket';

export function GoogleButton() {
  const [disable, setDisable] = React.useState(false);

  function handleLogin(response) {
    const fullname = response.profileObj.name;
    const emailAdress = response.profileObj.email;
    const avatarLink = response.profileObj.imageUrl;
    Socket.emit('new google user', {
      name: fullname,
      email: emailAdress,
      avatar: avatarLink,
    });
    setDisable(true);
  }

  return (
    <GoogleLogin
      clientId="477035920625-38n6lbf1m04mtpsfnvsiogmp4dlin790.apps.googleusercontent.com"
      buttonText="Sign in with Google"
      onSuccess={handleLogin}
      inSignedIn
      disabled={disable}
      cookiePolicy="single_host_origin"
    />
  );
}
