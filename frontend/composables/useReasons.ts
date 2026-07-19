import type { ReasonSearch } from '~/shared/types/reasons'
import type { ItemsTotal, Message } from '~/shared/types/utils'

export const useReasons = () => {
  const { notify } = useSnackbar()
  const reasonsDialog = useState('reasonsDialog', () => false)
  const categoryId = useState('categoryId', () => null)
  const items = useState('items', () => new Array())
  const total = useState('total', () => 0)

  const getReasons = async ({
    reasonsIds,
    categoryId = undefined,
    name = '',
    slug = '',
    description = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: ReasonSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>(`/api/reasons/search`, {
        body: {
          reasonsIds,
          categoryId: categoryId,
          name,
          slug,
          description,
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

  const create = async (body: any) => {
    return $api<Message>('/api/reasons', {
      method: 'POST',
      body,
    })
  }

  const get = async (id: number) => {
    return await $api(`/api/reasons/${id}`, {
      method: 'GET',
    })
  }

  const update = async (id: number, body: any) => {
    return await $api<Message>(`/api/reasons/${id}`, {
      method: 'PUT',
      body,
    })
  }

  const remove = async (id: number) => {
    return await $api<Message>(`/api/reasons/${id}`, {
      method: 'DELETE',
    })
  }

  return {
    items,
    total,
    reasonsDialog,
    categoryId,
    getReasons,
    create,
    get,
    update,
    remove,
  }
}
