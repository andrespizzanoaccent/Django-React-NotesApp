import { mount } from '@vue/test-utils';
import NoteEditor from '@/components/NoteEditor.vue';
import axios from 'axios';

jest.mock('axios');

const mockCategories = [
  { id: 1, name: 'Category 1' },
  { id: 2, name: 'Category 2' }
];

axios.get.mockResolvedValue({ data: mockCategories });

const mockNote = {
  id: 1,
  title: 'Test Note',
  content: 'Test Content',
  category_id: 1
};

describe('NoteEditor.vue', () => {
  it('fetches categories on mount and displays them in a dropdown', async () => {
    const wrapper = mount(NoteEditor, {
      props: { note: mockNote }
    });

    await wrapper.vm.$nextTick();

    const options = wrapper.findAll('option');
    expect(options).toHaveLength(mockCategories.length);
    expect(options.at(0).text()).toBe('Category 1');
    expect(options.at(1).text()).toBe('Category 2');
  });

  it('saves note with selected category', async () => {
    axios.put.mockResolvedValue({});

    const wrapper = mount(NoteEditor, {
      props: { note: mockNote }
    });

    await wrapper.vm.$nextTick();

    await wrapper.find('button').trigger('click');

    expect(axios.put).toHaveBeenCalledWith('/api/notes/1', mockNote);
  });
});
