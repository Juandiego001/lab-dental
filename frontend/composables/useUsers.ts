import type { UserSearch } from '~/shared/types/users'
import type { ItemsTotal } from '~/shared/types/utils'

export const useUsers = () => {
  const { notify } = useSnackbar()
  const items: any = ref([])
  const total: any = ref(15)

  const getUsers = async ({
    usersIds,
    distributorId,
    isMain = false,
    role = '',
    fullName = '',
    username = '',
    email = '',
    page = 1,
    perPage = 15,
    sortBy = undefined,
  }: UserSearch): Promise<void> => {
    try {
      const data = await $api<ItemsTotal>('/api/users/search', {
        body: {
          usersIds,
          distributorId,
          isMain,
          role,
          fullName,
          username,
          email,
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
    getUsers,
  }
}
