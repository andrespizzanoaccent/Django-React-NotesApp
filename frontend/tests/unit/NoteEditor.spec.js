import { shallowMount } from '@vue/test-utils';
import NoteEditor from '@/components/NoteEditor.vue';
import axios from 'axios';

jest.mock('axios');

describe('NoteEditor.vue', () => {
  it('fetches categories on creation', async () => {
    axios.get.mockResolvedValue({ data: [{ id: 1, name: 'Work' }] });
    const wrapper = shallowMount(NoteEditor);
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.categories).toEqual([{ id: 1, name: 'Work' }]);
  });

  it('handles save note failure', async () => {
    axios.post.mockRejectedValue(new Error('Failed to save note'));
    const wrapper = shallowMount(NoteEditor);
    wrapper.setData({ note: { title: 'Test', content: 'Content', category_id: 1 } });
    await wrapper.vm.saveNote();
    expect(wrapper.vm.categories).toEqual([]);
  });
});
