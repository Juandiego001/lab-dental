import type { WarrantyFilesSearch } from '~/shared/types/warranties'
import type { ItemsTotal } from '~/shared/types/utils'

export const useWarrantiesFiles = () => {
  const { notify } = useSnackbar()
  const tableDialog = useState('warrantyFilesTable', () => false)
  const warrantyId = useState('warrantyFilesWarrantyId', () => null)
  const items = useState('items', () => new Array())
  const total = useState('total', () => 0)

  const getWarrantyFiles = async ({
    title = '',
    description = '',
    originalName = '',
    extension = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: WarrantyFilesSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>(
        `/api/warranties/${warrantyId.value}/files/search`,
        {
          body: {
            warrantyId: warrantyId.value,
            title,
            description,
            originalName,
            extension,
            page,
            perPage,
            sortBy: sortBy,
          },
          method: 'POST',
        },
      )
      items.value = data.items
      total.value = data.total
    } catch (err) {
      notify(err, 'error')
    }
  }

  return {
    items,
    total,
    tableDialog,
    getWarrantyFiles,
    warrantyId,
  }
}
