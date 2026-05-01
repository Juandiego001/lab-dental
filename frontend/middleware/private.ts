export default defineNuxtRouteMiddleware(async (to, from) => {
  const { setProfile } = useProfile()
  const { $ability, $i18n } = useNuxtApp()

  try {
    const data: any = await $api(`/api/users/profile`)

    if (!data || !data.email) {
      setProfile(null)
      return navigateTo('/login')
    }

    if (data.abilities) $ability.update(data.abilities)
    setProfile(data)
    await $i18n.setLocale(data.language)
  } catch (err) {
    setProfile(null)
    return navigateTo('/login')
  }
})
