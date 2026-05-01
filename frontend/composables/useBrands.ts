import type { BrandSearch } from '~/shared/types/brands'
import type { ItemsTotal } from '~/shared/types/utils'

export const useBrands = () => {
  const { notify } = useSnackbar()
  const items: any = ref([])
  const total: any = ref(15)

  const getBrands = async ({
    brandsIds,
    name = '',
    slug = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: BrandSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>('/api/brands/search', {
        body: {
          brandsIds,
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
    getBrands,
  }
}
