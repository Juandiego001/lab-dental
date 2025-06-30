export const useProfile = () => {
  const profile = useState('profile', () => null)

  const setProfile = (profileData: any) => {
    profile.value = profileData
  }

  return {
    profile,
    setProfile
  }
}
