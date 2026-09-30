export const useProfile = () => {
  const profile = useState('profile', () => ({
    distributor_id: '',
    full_name: '',
    role: '',
    email: '',
    abilities: '',
    photo: '',
  }))

  const setProfile = (profileData: any) => {
    profile.value = profileData
  }

  const setPhoto = (photo: string) => {
    profile.value.photo = photo
  }

  const isAdmin = computed(() => profile.value.role === 'ADMIN')

  return {
    profile,
    setProfile,
    isAdmin,
    setPhoto,
  }
}
