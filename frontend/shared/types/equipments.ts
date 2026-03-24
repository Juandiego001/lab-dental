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

export interface EquipmentFilesSearch extends Pagination {
  equipmentId?: number
  title?: string
  description?: string
  originalName?: string
  extension?: string
}
