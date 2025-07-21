export default defineNuxtRouteMiddleware(async (to, from) => {
  if (import.meta.server) return
  const { setProfile } = useProfile();
  const { $ability } = useNuxtApp();
  try {
    const data: any = await $api(`/api/users/profile`);
    if (!data) {
      setProfile(null);
      return navigateTo('/login');
    }
    if (!data.email) {
      setProfile(null);
      return navigateTo('/login');
    }
    if (data.abilities) $ability.update(data.abilities)
    setProfile(data);
  } catch (err) {
    console.error(err);
    return navigateTo('/login')
  }
})
