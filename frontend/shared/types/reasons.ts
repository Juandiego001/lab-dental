import type { Pagination } from './utils'

export interface ReasonSearch extends Pagination {
  categoryId?: number
  name?: string
  slug?: string
  description?: string
}