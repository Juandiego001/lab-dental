export interface Group {
  createdAt: string;
  distributorId: number;
  distributorName: string;
  id: number;
  name: string;
  status: string;
  updatedAt: string;
}

export interface GroupForm {
    id?: number;
    name?: string;
    distributorId?: string;
    distributorName?: string;
    usersIds?: number[]
}