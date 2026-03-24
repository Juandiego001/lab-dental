import type { Pagination } from "./utils";

export interface DistributorSearch extends Pagination {
  distributorsIds: number[];
  name?: string;
}

export interface ContactSearch extends Pagination {
  distributorId: number;
  fullName?: string;
  email?: string;
  phone?: string;
}