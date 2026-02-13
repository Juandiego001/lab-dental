import type { Pagination } from "./utils";

export interface ClientSearch extends Pagination {
  distributorId?: number;
  clientId?: number;
  name?: string;
  phone?: string;
}