import React from 'react';

function Header({ toggleTheme }) {
  return (
    <header>
      <h1>App Header</h1>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  );
}

export default Header;
