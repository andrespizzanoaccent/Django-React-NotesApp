import React from 'react'

const Header = ({ darkMode, toggleTheme }) => {

    return (
        <div className="app-header">
            <h1>Note List</h1>
            <button onClick={toggleTheme} title="Toggle theme">
                {darkMode ? '☀️' : '🌙'}
            </button>
        </div>
    )
}

export default Header
