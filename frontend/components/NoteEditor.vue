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
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  props: ['note'],
  setup(props) {
    const categories = ref([]);

    const fetchCategories = async () => {
      try {
        const response = await axios.get('/api/categories');
        categories.value = response.data;
      } catch (error) {
        console.error('Failed to fetch categories:', error);
      }
    };

    onMounted(() => {
      fetchCategories();
    });

    const saveNote = async () => {
      try {
        await axios.put(`/api/notes/${props.note.id}`, props.note);
        alert('Note saved successfully!');
      } catch (error) {
        console.error('Failed to save note:', error);
      }
    };

    return {
      categories,
      saveNote
    };
  }
};
</script>
