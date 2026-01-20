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

  return {
    profile,
    setProfile
  }
}
