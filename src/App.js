import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import './App.css';

function App() {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setTheme(savedTheme);
      document.body.className = savedTheme;
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.body.className = newTheme;
    localStorage.setItem('theme', newTheme);
  };

  return (
    <div className="App">
      <Header toggleTheme={toggleTheme} />
      <main>
        <h1>Welcome to the Theme Toggle App</h1>
      </main>
    </div>
  );
}

export default App;
