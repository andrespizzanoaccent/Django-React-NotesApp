import { mount } from '@vue/test-utils';
import NoteList from '@/components/NoteList.vue';
import axios from 'axios';

jest.mock('axios');

const mockNotes = [
  { id: 1, title: 'Note 1', category_id: 1 },
  { id: 2, title: 'Note 2', category_id: 2 }
];

const mockCategories = [
  { id: 1, name: 'Category 1' },
  { id: 2, name: 'Category 2' }
];

axios.get.mockImplementation(url => {
  if (url === '/api/notes') {
    return Promise.resolve({ data: mockNotes });
  } else if (url === '/api/categories') {
    return Promise.resolve({ data: mockCategories });
  }
});

describe('NoteList.vue', () => {
  it('fetches notes and categories on mount and displays them', async () => {
    const wrapper = mount(NoteList);

    await wrapper.vm.$nextTick();

    const noteItems = wrapper.findAll('li');
    expect(noteItems).toHaveLength(mockNotes.length);
    expect(noteItems.at(0).text()).toBe('Note 1');
    expect(noteItems.at(1).text()).toBe('Note 2');
  });

  it('filters notes by selected category', async () => {
    const wrapper = mount(NoteList);

    await wrapper.vm.$nextTick();

    await wrapper.find('select').setValue('1');

    const noteItems = wrapper.findAll('li');
    expect(noteItems).toHaveLength(1);
    expect(noteItems.at(0).text()).toBe('Note 1');
  });
});
