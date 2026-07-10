import type { Pagination } from './utils'

export interface WarrantyPartSearch extends Pagination {
  equipmentId?: number
  partNumber?: string
  description?: string
  partId?: number
  invoiceParts?: string
}
