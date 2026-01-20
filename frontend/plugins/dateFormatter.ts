export default defineNuxtPlugin((app) => {
  const dateFormat = (theDate: any) => {
    const [month, day, year] = theDate.toLocaleString('en-US', { day: '2-digit', month: 'long', year: 'numeric' }).toUpperCase().replace(',', '').split(' ')
    return `${day} ${month} ${year}`
  }

  return {
    provide: {
      dateFormat
    }
  }
})