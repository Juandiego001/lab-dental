import type { Pagination } from "./utils";

export interface BrandSearch extends Pagination {
  brandId?: number;
  name?: string;
  slug?: string;
}