import React, { useState, useEffect } from 'react';
import ListItem from '../components/ListItem';
import AddButton from '../components/AddButton';

const NotesListPage = () => {
    const [notes, setNotes] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');

    useEffect(() => {
        getNotes();
        getCategories();
    }, [selectedCategory]);

    const getNotes = async () => {
        let url = '/api/notes/';
        if (selectedCategory) {
            url += `?category=${selectedCategory}`;
        }
        const response = await fetch(url);
        const data = await response.json();
        setNotes(data);
    };

    const getCategories = async () => {
        const response = await fetch('/api/categories/');
        const data = await response.json();
        setCategories(data);
    };

    return (
        <div className="notes">
            <div className="notes-header">
                <h2 className="notes-title">&#9782; Notes</h2>
                <p className="notes-count">{notes.length}</p>
            </div>
            <div className="category-filter">
                <select
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    value={selectedCategory}
                >
                    <option value="">All Categories</option>
                    {categories.map((category) => (
                        <option key={category.id} value={category.id}>
                            {category.name}
                        </option>
                    ))}
                </select>
            </div>
            <div className="notes-list">
                {notes.map((note, index) => (
                    <ListItem key={index} note={note} />
                ))}
            </div>
            <AddButton />
        </div>
    );
};

export default NotesListPage;
