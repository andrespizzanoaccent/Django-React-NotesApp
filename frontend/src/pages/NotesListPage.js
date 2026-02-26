import React, { useState, useEffect } from 'react'
import ListItem from '../components/ListItem'
import AddButton from '../components/AddButton'


const NotesListPage = () => {

    let [notes, setNotes] = useState([])
    let [categories, setCategories] = useState([])
    let [selectedCategory, setSelectedCategory] = useState('')

    useEffect(() => {
        getNotes()
        getCategories()
    }, [])

    let getNotes = async () => {
        try {
            let response = await fetch('/api/notes/')
            if (!response.ok) throw new Error('Failed to fetch notes')
            let data = await response.json()
            setNotes(data)
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

    let filterNotesByCategory = (categoryId) => {
        setSelectedCategory(categoryId)
        if (categoryId === '') {
            getNotes()
        } else {
            setNotes(notes.filter(note => note.category === categoryId))
        }
    }

    return (
        <div className="notes">
            <div className="notes-header">
                <h2 className="notes-title">&#9782; Notes</h2>
                <p className="notes-count">{notes.length}</p>
            </div>

            <div className="category-filter">
                <select onChange={(e) => filterNotesByCategory(e.target.value)} value={selectedCategory}>
                    <option value="">All Categories</option>
                    {categories.map(category => (
                        <option key={category.id} value={category.id}>{category.name}</option>
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
    )
}

export default NotesListPage
