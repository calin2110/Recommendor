export interface UserDto {
  firstName: string,
  lastName: string,
  email: string,
  genre: string | null,
  canBeDeleted: boolean,
  ratingsCount: number
}
