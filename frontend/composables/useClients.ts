import type { ClientSearch } from '~/shared/types/clients'
import type { ItemsTotal } from '~/shared/types/utils'

export const useClients = () => {
  const { notify } = useSnackbar()
  const items: any = ref([])
  const total: any = ref(15)

  const getClients = async ({
    distributorId,
    clientId,
    name = '',
    phone = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: ClientSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>('/api/clients/search', {
        body: {
          distributorId,
          clientId,
          name,
          phone,
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
    getClients,
  }
}
