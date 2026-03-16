export const useProfile = () => {
  const profile = useState('profile', () => ({
    distributor_id: '',
    full_name: '',
    role: '',
    email: '',
    abilities: '',
    photoPath: '',
  }))

  const setProfile = (profileData: any) => {
    profile.value = profileData
  }

  const setPhotoPath = (photoPath: string) => {
    profile.value.photoPath = photoPath
  }

  const isAdmin = computed(() => profile.value.role === 'ADMIN');

  return {
    profile,
    setProfile,
    isAdmin,
    setPhotoPath
  }
}
