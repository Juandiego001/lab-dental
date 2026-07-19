import type { Pagination } from './utils'

export interface ReasonSearch extends Pagination {
  reasonsIds?: number[]
  categoryId?: number
  name?: string
  slug?: string
  description?: string
}