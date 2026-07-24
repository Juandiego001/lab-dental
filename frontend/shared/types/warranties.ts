import type { Pagination } from './utils'

export interface WarrantyFilesSearch extends Pagination {
  warrantyId?: number
  title?: string
  description?: string
  originalName?: string
  extension?: string
}
