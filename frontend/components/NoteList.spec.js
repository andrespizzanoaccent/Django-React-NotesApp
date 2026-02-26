import { mount } from '@vue/test-utils';
import NoteList from '@/components/NoteList.vue';
import axios from 'axios';
import flushPromises from 'flush-promises';

jest.mock('axios');

const notesMock = [
  { id: 1, title: 'Note 1', categoryId: 1 },
  { id: 2, title: 'Note 2', categoryId: 2 }
];

const categoriesMock = [
  { id: 1, name: 'Work' },
  { id: 2, name: 'Personal' }
];

axios.get.mockImplementation((url) => {
  if (url === '/api/notes') {
    return Promise.resolve({ data: notesMock });
  } else if (url === '/api/categories') {
    return Promise.resolve({ data: categoriesMock });
  }
});

describe('NoteList.vue', () => {
  it('filters notes by category', async () => {
    const wrapper = mount(NoteList);

    await flushPromises();

    const select = wrapper.find('select');
    await select.setValue('1');

    const noteItems = wrapper.findAll('li');
    expect(noteItems).toHaveLength(1);
    expect(noteItems.at(0).text()).toBe('Note 1');
  });

  it('shows all notes when no category is selected', async () => {
    const wrapper = mount(NoteList);

    await flushPromises();

    const select = wrapper.find('select');
    await select.setValue('');

    const noteItems = wrapper.findAll('li');
    expect(noteItems).toHaveLength(2);
  });
});
