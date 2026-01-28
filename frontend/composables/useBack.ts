export const useBack = () => {
  const { $ability } = useNuxtApp()

  const back = () => {
    let goTo = '/app'
    if (history.state?.back) {
      const prevModule = history.state.back.split('/app/')[1]
      if (prevModule && $ability.can('read', prevModule))
        goTo = `/app/${prevModule}`
    }

    navigateTo(goTo)
  }

  return {
    back
  }
}
