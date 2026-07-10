import type { ContactSearch } from '~/shared/types/distributors'
import type { ItemsTotal } from '~/shared/types/utils'

export const useContacts = () => {
  const { notify } = useSnackbar()
  const items: any = ref([])
  const total: any = ref(0)
  const distributorId = useState('distributorId', () => null)
  const dialog = useState('dialog', () => false)

  const getContacts = async ({
    theDistributorId = undefined,
    fullName = '',
    email = '',
    phone = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: ContactSearch): Promise<ItemsTotal> => {
    try {
      const data = await $api<ItemsTotal>(`/api/distributors/contacts/search`, {
        body: {
          distributorId: theDistributorId || distributorId.value,
          fullName,
          email,
          phone,
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
    getContacts,
    dialog,
    distributorId,
  }
}
