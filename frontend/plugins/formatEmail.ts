export default defineNuxtPlugin(() => {
  const formatEmail = (v?: string) => {
    if (!v) return ''

    return v.toLowerCase().replace(/[^a-z0-9@._-]/g, '')
  }

  return {
    provide: {
      formatEmail,
    },
  }
})
