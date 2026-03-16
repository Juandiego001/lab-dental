import type { Pagination } from './utils'

export interface EquipmentSearch extends Pagination {
  equipmentId?: number
  brandId?: number
  categoryId?: number
  model?: string
  reference?: string
  modelReference?: string
  withPicture?: boolean
}
