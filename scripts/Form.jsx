import * as React from 'react';
import { Socket } from './Socket';
import { SubmitButton } from './SubmitButton';

export function Form() {
  const [text, setText] = React.useState('');
  // Current input being typed in the input box

  function handleSubmit(e) {
    e.preventDefault();
    Socket.emit('new message sent', {
      message: text,
    });
    setText('');
  }

  function handleChange(e) {
    setText(e.target.value);
    if (e.key === 'Enter') {
      handleSubmit();
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={text} onChange={handleChange} maxLength="1000" />
      <SubmitButton />
    </form>
  );
}
