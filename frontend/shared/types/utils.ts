export interface ItemsTotal {
  items: any[]
  total: number
}

export interface SortBy {
  key: string
  order: string
}

export interface Pagination {
  page: number
  perPage: number
  sortBy?: SortBy
}


export interface Message {
  message: string
}