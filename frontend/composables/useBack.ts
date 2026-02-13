export const useBack = () => {
  const { $ability } = useNuxtApp()

  const back = (backTo?: string) => {
    let goTo = backTo || '/app'
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
