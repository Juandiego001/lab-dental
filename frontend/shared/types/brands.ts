import type { Pagination } from "./utils";

export interface BrandSearch extends Pagination {
  brandsIds?: number;
  name?: string;
  slug?: string;
}