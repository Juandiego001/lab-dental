import type { Pagination } from "./utils";

export interface CategorySearch extends Pagination {
  categoryId?: number;
  name?: string;
  slug?: string;
}