export default defineNuxtPlugin(() => {
  const generateSlug = (text: string) => {
    if (!text) return ''

    return (
      text
        .toString()
        // 1. Separa las letras de sus acentos/tildes
        .normalize('NFD')
        // 2. Elimina los acentos (marcas diacríticas)
        .replace(/[\u0300-\u036f]/g, '')
        // 3. Convierte todo a minúsculas
        .toLowerCase()
        // 4. Reemplaza uno o más espacios por un solo guion
        .replace(/\s+/g, '-')
        // 5. Elimina cualquier carácter que no sea a-z, 0-9 o un guion
        .replace(/[^a-z0-9-]/g, '')
        // 6. Evita que queden guiones repetidos juntos (ej: "hola---mundo" -> "hola-mundo")
        .replace(/-+/g, '-')
    )
  }

  return {
    provide: {
      generateSlug,
    },
  }
})
