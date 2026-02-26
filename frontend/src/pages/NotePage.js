import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';

const NotePage = () => {
    const { id } = useParams();
    const history = useHistory();
    const [note, setNote] = useState({ body: '', category: null });
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        if (id !== 'new') {
            fetchNote();
        }
        fetchCategories();
    }, [id]);

    const fetchNote = async () => {
        const response = await fetch(`/api/notes/${id}/`);
        const data = await response.json();
        setNote(data);
    };

    const fetchCategories = async () => {
        const response = await fetch('/api/categories/');
        const data = await response.json();
        setCategories(data);
    };

    const handleSubmit = async () => {
        if (id === 'new' && note.body) {
            await fetch(`/api/notes/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(note),
            });
        } else if (id !== 'new') {
            await fetch(`/api/notes/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(note),
            });
        }
        history.push('/');
    };

    const handleDelete = async () => {
        await fetch(`/api/notes/${id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        history.push('/');
    };

    return (
        <div className="note">
            <textarea
                onChange={(e) => setNote({ ...note, body: e.target.value })}
                value={note.body}
            ></textarea>
            <select
                onChange={(e) => setNote({ ...note, category: e.target.value })}
                value={note.category || ''}
            >
                <option value="">No Category</option>
                {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                        {category.name}
                    </option>
                ))}
            </select>
            <button onClick={handleSubmit}>Save</button>
            {id !== 'new' && <button onClick={handleDelete}>Delete</button>}
        </div>
    );
};

export default NotePage;
