import type { Pagination } from './utils'

export interface DistributorSearch extends Pagination {
  distributorsIds: number[]
  name?: string
  bp?: string
}

export interface ContactSearch extends Pagination {
  theDistributorId?: number
  contactsIds?: number[]
  fullName?: string
  email?: string
  phone?: string
}

export interface DistributorAlignerSearch extends Pagination {
  theDistributorId?: number
  alignersIds?: number[]
  serial?: string
  software?: string
}
