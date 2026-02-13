import type { Pagination } from "./utils";

export interface SiteSearch extends Pagination {
  siteId?: number;
  distributorId?: number;
  clientId?: number;
  name?: string;
}