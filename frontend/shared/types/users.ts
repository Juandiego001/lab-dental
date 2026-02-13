import type { Pagination } from './utils'

export interface UserSearch extends Pagination {
  usersIds?: number[]
  distributorId?: number
  isMain?: boolean;
  role?: string;
  fullName?: string
  username?: string
  email?: string
}
