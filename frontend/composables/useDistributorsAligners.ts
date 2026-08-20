import type { DistributorAlignerSearch } from '~/shared/types/distributors'
import type { ItemsTotal } from '~/shared/types/utils'

export const useDistributorsAligners = () => {
  const { notify } = useSnackbar()
  const items: any = useState('distributorsAlignersItems', () => new Array(0))
  const total: any = useState('totalDistributorsAligners', () => 0)
  const distributorId = useState('distributorId', () => null)
  const dialog = useState('distributorsAlignersDialog', () => false)
  const loading = useState('loadingDistributorsAligners', () => false)

  const getAligners = async ({
    theDistributorId = undefined,
    alignersIds,
    serial = '',
    software = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: DistributorAlignerSearch): Promise<ItemsTotal> => {
    try {
      loading.value = true;
      const data = await $api<ItemsTotal>(`/api/distributors/aligners/search`, {
        body: {
          distributorId: theDistributorId || distributorId.value,
          alignersIds: alignersIds,
          serial,
          software,
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
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    total,
    getAligners,
    dialog,
    distributorId,
    loading
  }
}
