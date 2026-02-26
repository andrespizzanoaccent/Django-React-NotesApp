<template>
  <div>
    <input v-model="note.title" placeholder="Title" />
    <textarea v-model="note.content" placeholder="Content"></textarea>
    <select v-model="note.category_id">
      <option v-for="category in categories" :key="category.id" :value="category.id">
        {{ category.name }}
      </option>
    </select>
    <button @click="saveNote">Save</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      note: {
        title: '',
        content: '',
        category_id: null
      },
      categories: []
    };
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get('/api/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('Failed to fetch categories:', error);
      }
    },
    async saveNote() {
      try {
        await axios.post('/api/notes/', this.note);
        alert('Note saved successfully');
      } catch (error) {
        console.error('Failed to save note:', error);
        alert('Failed to save note');
      }
    }
  },
  created() {
    this.fetchCategories();
  }
};
</script>
