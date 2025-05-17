export default defineNuxtRouteMiddleware(async (to, from) => {  
  const { $ability } = useNuxtApp();
  try {
    const headers = useRequestHeaders(['cookie'])
    const { data } = await useFetch<any>('http://localhost:3000/api/users/profile', {
      method: 'GET',
      headers: {
        ...(headers?.cookie ? { cookie: headers.cookie } : {})
      }
    });
    if (!data.value.email) return navigateTo('/login');
    if (data.value.abilities) $ability.update(data.value.abilities)
  } catch (err) {
    console.error(err);
    return navigateTo('/login')
  }
})
