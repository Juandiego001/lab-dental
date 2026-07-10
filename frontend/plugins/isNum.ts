export default defineNuxtPlugin(() => {
  function isNum(val: any) {
    return val !== null && val !== '' && !Number.isNaN(Number(val))
  }

  return {
    provide: {
      isNum,
    },
  }
})
