import { mount } from '@vue/test-utils';
import NoteEditor from '@/components/NoteEditor.vue';
import axios from 'axios';

jest.mock('axios');

const categories = [
  { id: 1, name: 'Work' },
  { id: 2, name: 'Personal' }
];

axios.get.mockResolvedValue({ data: categories });

describe('NoteEditor.vue', () => {
  it('renders category options', async () => {
    const wrapper = mount(NoteEditor, {
      props: { note: { title: '', content: '', category_id: null } }
    });

    await wrapper.vm.$nextTick(); // Wait for promises to resolve

    const options = wrapper.findAll('option');
    expect(options).toHaveLength(categories.length);
    expect(options.at(0).text()).toBe('Work');
    expect(options.at(1).text()).toBe('Personal');
  });

  it('saves a note with a category', async () => {
    const wrapper = mount(NoteEditor, {
      props: { note: { title: 'Test', content: 'Content', category_id: 1 } }
    });

    axios.post.mockResolvedValue({});

    await wrapper.find('button').trigger('click');

    expect(axios.post).toHaveBeenCalledWith('/api/notes', {
      title: 'Test',
      content: 'Content',
      category_id: 1
    });
  });
});
