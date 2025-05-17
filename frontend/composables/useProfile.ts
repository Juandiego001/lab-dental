import { useCookie } from '#app'

export interface UserProfile {
  id: Number
  full_name: string
  email: string
}

export const useProfile = () => {
  return useCookie<UserProfile | null>('profile', {
    default: () => null,
    watch: true
  })
}
