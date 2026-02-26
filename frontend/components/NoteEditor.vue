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

    onMounted(async () => {
      const response = await axios.get('/api/categories');
      categories.value = response.data;
    });

    const saveNote = async () => {
      if (props.note.id) {
        await axios.put(`/api/notes/${props.note.id}`, props.note);
      } else {
        await axios.post('/api/notes', props.note);
      }
    };

    return { categories, saveNote };
  }
};
</script>
