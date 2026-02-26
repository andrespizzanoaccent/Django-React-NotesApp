<template>
  <div>
    <input v-model="note.title" placeholder="Note Title" />
    <textarea v-model="note.content" placeholder="Note Content"></textarea>
    <select v-model="note.categoryId">
      <option v-for="category in categories" :key="category.id" :value="category.id">
        {{ category.name }}
      </option>
    </select>
    <button @click="saveNote">Save Note</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  props: ['note'],
  setup(props) {
    const categories = ref([]);

    onMounted(async () => {
      const response = await axios.get('/api/categories');
      categories.value = response.data;
    });

    const saveNote = async () => {
      // Logic to save the note
    };

    return {
      categories,
      saveNote
    };
  }
};
</script>
