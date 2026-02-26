<template>
  <div>
    <select v-model="selectedCategory" @change="filterNotes">
      <option value="">All Categories</option>
      <option v-for="category in categories" :key="category.id" :value="category.id">
        {{ category.name }}
      </option>
    </select>
    <ul>
      <li v-for="note in filteredNotes" :key="note.id">
        {{ note.title }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      notes: [],
      categories: [],
      selectedCategory: ''
    };
  },
  computed: {
    filteredNotes() {
      if (!this.selectedCategory) return this.notes;
      return this.notes.filter(note => note.category_id === this.selectedCategory);
    }
  },
  methods: {
    async fetchNotes() {
      try {
        const response = await axios.get('/api/notes/');
        this.notes = response.data;
      } catch (error) {
        console.error('Failed to fetch notes:', error);
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('/api/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('Failed to fetch categories:', error);
      }
    },
    filterNotes() {
      // This method is triggered by the change event on the category select
    }
  },
  created() {
    this.fetchNotes();
    this.fetchCategories();
  }
};
</script>
