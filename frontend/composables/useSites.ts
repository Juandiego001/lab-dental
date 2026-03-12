import type { SiteSearch } from '~/shared/types/sites'
import type { ItemsTotal } from '~/shared/types/utils'

export const useSites = () => {
  const { notify } = useSnackbar()
  const items: any = ref([])
  const total: any = ref(15)

  const getSites = async ({
    siteId,
    distributorId,
    clientId,
    name = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: SiteSearch): Promise<ItemsTotal> => {
    try {
      const data = await $api<ItemsTotal>('/api/sites/search', {
        body: {
          siteId,
          distributorId,
          clientId,
          name,
          page,
          perPage,
          sortBy: sortBy,
        },
        method: 'POST',
      })
      items.value = data.items
      total.value = data.total
      return data
    } catch (err) {
      notify(err, 'error')
      return { items: [], total: 0 }
    }
  }

  return {
    items,
    total,
    getSites,
  }
}
