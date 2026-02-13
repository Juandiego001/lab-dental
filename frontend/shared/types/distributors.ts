import type { Pagination } from "./utils";

export interface DistributorSearch extends Pagination {
  distributorsIds: number[];
  name?: string;
}