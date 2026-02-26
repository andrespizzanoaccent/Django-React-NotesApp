<template>
  <div>
    <select v-model="selectedCategory">
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
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const notes = ref([]);
    const categories = ref([]);
    const selectedCategory = ref('');

    onMounted(async () => {
      const notesResponse = await axios.get('/api/notes');
      notes.value = notesResponse.data;

      const categoriesResponse = await axios.get('/api/categories');
      categories.value = categoriesResponse.data;
    });

    const filteredNotes = computed(() => {
      if (!selectedCategory.value) return notes.value;
      return notes.value.filter(note => note.category_id === selectedCategory.value);
    });

    return { notes, categories, selectedCategory, filteredNotes };
  }
};
</script>
