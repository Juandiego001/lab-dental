import type { EquipmentSearch } from '~/shared/types/equipments'
import type { ItemsTotal } from '~/shared/types/utils'

export const useEquipments = () => {
  const { notify } = useSnackbar()
  const items: any = ref([])
  const total: any = ref(15)

  const getEquipments = async ({
    equipmentId,
    brandId,
    categoryId,
    model = '',
    reference = '',
    modelReference = '',
    withPicture = true,
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: EquipmentSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>('/api/equipments/search', {
        body: {
          equipmentId,
          brandId,
          categoryId,
          model,
          reference,
          modelReference,
          withPicture,
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
    getEquipments,
  }
}
