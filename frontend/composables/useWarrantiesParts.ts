import type { WarrantyPartSearch } from '~/shared/types/warrantiesParts'
import type { ItemsTotal, Message } from '~/shared/types/utils'

export const useWarrantiesParts = () => {
  const { notify } = useSnackbar()
  const partsDialog = useState('partsDialog', () => false)
  const partData = useState('partData', () => ({
    partNumber: null,
    description: null,
    invoiceParts: null,
    quantity: null,
    price: null,
    total: null,
  }))
  const items: any = useState('itemsParts', () => new Array(0))
  const total: any = useState('totalParts', () => 0)

  const remove = (id: number) => {
    try {
      let partIndex = items.value.findIndex((e: any) => e.id === id)
      if (partIndex !== -1) {
        items.value.splice(partIndex, 1)
      }
    } catch (err) {}
  }

  return {
    items,
    total,
    partsDialog,
    partData,
    remove,
  }
}
