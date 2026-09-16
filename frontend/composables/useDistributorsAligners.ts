import type { DistributorAlignerSearch } from '~/shared/types/distributors'
import type { ItemsTotal } from '~/shared/types/utils'

export const useDistributorsAligners = () => {
  const { notify } = useSnackbar()
  const items: any = useState('distributorsAlignersItems', () => new Array(0))
  const total: any = useState('totalDistributorsAligners', () => 0)
  const distributorId = useState('distributorId', () => null)
  const dialog = useState('distributorsAlignersDialog', () => false)
  const loading = useState('loadingDistributorsAligners', () => false)

  return {
    items,
    total,
    dialog,
    distributorId,
    loading,
  }
}
