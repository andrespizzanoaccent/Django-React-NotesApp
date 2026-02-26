import { mount } from '@vue/test-utils';
import NoteList from '@/components/NoteList.vue';
import axios from 'axios';

jest.mock('axios');

const notes = [
  { id: 1, title: 'Note 1', category_id: 1 },
  { id: 2, title: 'Note 2', category_id: 2 }
];

const categories = [
  { id: 1, name: 'Work' },
  { id: 2, name: 'Personal' }
];

axios.get.mockImplementation(url => {
  if (url === '/api/notes') return Promise.resolve({ data: notes });
  if (url === '/api/categories') return Promise.resolve({ data: categories });
});

describe('NoteList.vue', () => {
  it('renders notes filtered by category', async () => {
    const wrapper = mount(NoteList);

    await wrapper.vm.$nextTick(); // Wait for promises to resolve

    wrapper.find('select').setValue('1');

    await wrapper.vm.$nextTick();

    const listItems = wrapper.findAll('li');
    expect(listItems).toHaveLength(1);
    expect(listItems.at(0).text()).toBe('Note 1');
  });
});
