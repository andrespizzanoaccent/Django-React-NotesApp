import React, { useState, useEffect } from 'react'
import { useParams, useHistory } from 'react-router-dom'


const NotePage = () => {
    let { id } = useParams()
    let history = useHistory()
    let [note, setNote] = useState(null)
    let [categories, setCategories] = useState([])

    useEffect(() => {
        getNote()
        getCategories()
    }, [id])

    let getNote = async () => {
        if (id === 'new') return

        try {
            let response = await fetch(`/api/notes/${id}/`)
            if (!response.ok) throw new Error('Failed to fetch note')
            let data = await response.json()
            setNote(data)
        } catch (error) {
            console.error(error)
        }
    }

    let getCategories = async () => {
        try {
            let response = await fetch('/api/categories/')
            if (!response.ok) throw new Error('Failed to fetch categories')
            let data = await response.json()
            setCategories(data)
        } catch (error) {
            console.error(error)
        }
    }

    let createNote = async () => {
        fetch(`/api/notes/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(note)
        }).then(response => {
            if (!response.ok) throw new Error('Failed to create note')
            history.push('/')
        }).catch(error => console.error(error))
    }

    let updateNote = async () => {
        fetch(`/api/notes/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(note)
        }).then(response => {
            if (!response.ok) throw new Error('Failed to update note')
            history.push('/')
        }).catch(error => console.error(error))
    }

    let deleteNote = async () => {
        fetch(`/api/notes/${id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (!response.ok) throw new Error('Failed to delete note')
            history.push('/')
        }).catch(error => console.error(error))
    }

    let handleSubmit = () => {
        if (id !== 'new' && note.body === '') {
            deleteNote()
        } else if (id !== 'new') {
            updateNote()
        } else if (id === 'new' && note !== null) {
            createNote()
        }
    }

    return (
        <div className="note">
            <div className="note-header">
                <h3>
                    <button onClick={handleSubmit}>Save</button>
                </h3>
            </div>
            <textarea onChange={(e) => { setNote({ ...note, 'body': e.target.value }) }} value={note?.body}></textarea>
            <select onChange={(e) => { setNote({ ...note, 'category': e.target.value }) }} value={note?.category || ''}>
                <option value="">Select Category</option>
                {categories.map(category => (
                    <option key={category.id} value={category.id}>{category.name}</option>
                ))}
            </select>
        </div>
    )
}

export default NotePage
