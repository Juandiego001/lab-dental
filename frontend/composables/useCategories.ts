import type { CategorySearch } from '~/shared/types/categories'
import type { ItemsTotal } from '~/shared/types/utils'

export const useCategories = () => {
  const { notify } = useSnackbar()
  const items: any = ref([])
  const total: any = ref(15)

  const getCategories = async ({
    categoryId,
    name = '',
    slug = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: CategorySearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>('/api/categories/search', {
        body: {
          categoryId,
          name,
          slug,
          page,
          perPage,
          sortBy: sortBy,
        },
        method: 'POST',
      })
      items.value = data.items
      total.value = data.total
    } catch (err) {
      notify(err, 'error')
    }
  }

  return {
    items,
    total,
    getCategories,
  }
}
