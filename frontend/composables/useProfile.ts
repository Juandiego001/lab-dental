export const useProfile = () => {
  const profile = useState('profile', () => ({
    distributor_id: '',
    full_name: '',
    role: '',
    email: '',
    abilities: '',
  }))

  const setProfile = (profileData: any) => {
    profile.value = profileData
  }

  const isAdmin = computed(() => profile.value.role === 'ADMIN');

  return {
    profile,
    setProfile,
    isAdmin
  }
}
