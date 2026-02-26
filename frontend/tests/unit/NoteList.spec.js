import { shallowMount } from '@vue/test-utils';
import NoteList from '@/components/NoteList.vue';
import axios from 'axios';

jest.mock('axios');

describe('NoteList.vue', () => {
  it('fetches notes and categories on creation', async () => {
    axios.get.mockResolvedValueOnce({ data: [{ id: 1, title: 'Note 1', category_id: 1 }] });
    axios.get.mockResolvedValueOnce({ data: [{ id: 1, name: 'Work' }] });
    const wrapper = shallowMount(NoteList);
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.notes).toEqual([{ id: 1, title: 'Note 1', category_id: 1 }]);
    expect(wrapper.vm.categories).toEqual([{ id: 1, name: 'Work' }]);
  });

  it('filters notes by selected category', async () => {
    const wrapper = shallowMount(NoteList, {
      data() {
        return {
          notes: [
            { id: 1, title: 'Note 1', category_id: 1 },
            { id: 2, title: 'Note 2', category_id: 2 }
          ],
          selectedCategory: 1
        };
      }
    });
    expect(wrapper.vm.filteredNotes).toEqual([{ id: 1, title: 'Note 1', category_id: 1 }]);
  });
});
