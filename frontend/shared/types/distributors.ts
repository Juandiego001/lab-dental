import type { Pagination } from './utils'

export interface DistributorSearch extends Pagination {
  distributorsIds: number[]
  name?: string
}

export interface ContactSearch extends Pagination {
  theDistributorId?: number
  contactsIds?: number[]
  fullName?: string
  email?: string
  phone?: string
}
