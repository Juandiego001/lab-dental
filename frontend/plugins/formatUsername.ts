export default defineNuxtPlugin(() => {
  const formatUsername = (v?: string) => {
    if (!v) return ''

    return v.toLowerCase().replace(/[^a-z0-9._-]/g, '')
  }

  return {
    provide: {
      formatUsername,
    },
  }
})
