import type { DistributorSearch } from '~/shared/types/distributors'
import type { ItemsTotal } from '~/shared/types/utils'

export const useDistributors = () => {
  const { notify } = useSnackbar()
  const items: any = ref([])
  const total: any = ref(15)

  const getDistributors = async ({
    distributorsIds,
    name = '',
    bp = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: DistributorSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>('/api/distributors/search', {
        body: {
          distributorsIds,
          name,
          bp,
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
    getDistributors,
  }
}
