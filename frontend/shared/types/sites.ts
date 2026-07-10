import type { Pagination } from "./utils";

export interface SiteSearch extends Pagination {
  siteId?: number;
  distributorId?: number;
  clientId?: number;
  name?: string;
}

export interface Location {
  id?: number;
  name?: string;
}

export interface Address {
  id?: number;
  city?: Location;
  state?: Location;
  country?: Location;
}