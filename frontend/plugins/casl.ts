import { createMongoAbility } from '@casl/ability'

export default defineNuxtPlugin((app) => {
  const ability = createMongoAbility([]);
  return {
    provide: {
      ability
    }
  }
})
