import { mount } from '@vue/test-utils';
import NoteEditor from '@/components/NoteEditor.vue';
import axios from 'axios';
import flushPromises from 'flush-promises';

jest.mock('axios');

const categoriesMock = [
  { id: 1, name: 'Work' },
  { id: 2, name: 'Personal' }
];

axios.get.mockResolvedValue({ data: categoriesMock });

describe('NoteEditor.vue', () => {
  it('renders category options', async () => {
    const wrapper = mount(NoteEditor, {
      props: { note: { title: '', content: '', categoryId: null } }
    });

    await flushPromises();

    const options = wrapper.findAll('option');
    expect(options).toHaveLength(categoriesMock.length);
    expect(options.at(0).text()).toBe('Work');
    expect(options.at(1).text()).toBe('Personal');
  });

  it('assigns a category to a note', async () => {
    const wrapper = mount(NoteEditor, {
      props: { note: { title: '', content: '', categoryId: null } }
    });

    await flushPromises();

    const select = wrapper.find('select');
    await select.setValue('1');

    expect(wrapper.vm.note.categoryId).toBe('1');
  });
});
