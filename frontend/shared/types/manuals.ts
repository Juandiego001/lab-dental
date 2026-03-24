import type { Pagination } from './utils'

export interface ManualSearch extends Pagination {
  equipmentId?: number
  title?: string
  description?: string
  manualTypeId?: number
  originalName?: string
  extension?: string
}

export interface ManualTypeSearch extends Pagination {
  name?: string
  slug?: string
}


