import type { EquipmentFilesSearch } from '~/shared/types/equipments'
import type { ItemsTotal } from '~/shared/types/utils'

export const useEquipmentFiles = () => {
  const { notify } = useSnackbar()
  const tableDialog = useState('tableDialog', () => false)
  const sliderDialog = useState('sliderDialog', () => false)
  const equipmentId = useState('equipmentId', () => null)
  const items = useState('items', () => new Array())
  const total = useState('total', () => 0)

  const getEquipmentFiles = async ({
    title = '',
    description = '',
    originalName = '',
    extension = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: EquipmentFilesSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>(
        `/api/equipments/${equipmentId.value}/files/search`,
        {
          body: {
            equipmentId: equipmentId.value,
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
    sliderDialog,
    getEquipmentFiles,
    equipmentId,
  }
}
