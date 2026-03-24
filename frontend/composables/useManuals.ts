import type { ManualSearch, ManualTypeSearch } from '~/shared/types/manuals'
import type { ItemsTotal, Message } from '~/shared/types/utils'

export const useManuals = () => {
  const { notify } = useSnackbar()
  const manualsDialog = useState('manualsDialog', () => false)
  const equipmentId = useState('equipmentId', () => null)
  const items = useState('items', () => new Array())
  const total = useState('total', () => 0)
  const itemsTypes = useState('itemsTypes', () => new Array())
  const totalTypes = useState('totalTypes', () => 0)

  const getManuals = async ({
    equipmentId = undefined,
    title = '',
    description = '',
    manualTypeId = undefined,
    originalName = '',
    extension = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: ManualSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>(`/api/manuals/search`, {
        body: {
          equipmentId: equipmentId,
          title,
          description,
          manualTypeId: manualTypeId,
          originalName,
          extension,
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

  const create = async (formData: FormData) => {
    return $api<Message>('/api/manuals', {
      method: 'POST',
      body: formData,
    })
  }

  const get = async (id: number) => {
    return await $api(`/api/manuals/${id}`, {
      method: 'GET',
    })
  }

  const update = async (id: number, body: any) => {
    return await $api<Message>(`/api/manuals/${id}`, {
      method: 'PUT',
      body,
    })
  }

  const remove = async (id: number) => {
    return await $api<Message>(`/api/manuals/${id}`, {
      method: 'DELETE',
    })
  }

  const getManualTypes = async ({
    name = '',
    slug = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: ManualTypeSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>(`/api/manuals/types/search`, {
        body: {
          name,
          slug,
          page,
          perPage,
          sortBy: sortBy,
        },
        method: 'POST',
      })
      itemsTypes.value = data.items
      totalTypes.value = data.total
    } catch (err) {
      notify(err, 'error')
    }
  }

  return {
    items,
    total,
    manualsDialog,
    getManuals,
    get,
    create,
    update,
    remove,
    equipmentId,
    getManualTypes,
    itemsTypes,
    totalTypes,
  }
}
