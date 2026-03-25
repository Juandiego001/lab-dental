export function $api<T>(
  request: Parameters<typeof $fetch<T>>[0],
  opts?: Parameters<typeof $fetch<T>>[1],
) {
  const config = useRuntimeConfig()
  const csrf_access_token: any = useCookie('csrf_access_token').value
  const baseURL = import.meta.server ? (config.public.appUrl as string) : '/'
  console.log({ baseURL })
  let customHeaders: any = {
    'X-CSRF-TOKEN': csrf_access_token || '',
    ...opts?.headers,
  }

  if (import.meta.server) {
    const reqHeaders = useRequestHeaders(['cookie'])
    if (reqHeaders.cookie) customHeaders.cookie = reqHeaders.cookie
  } else {
    opts = opts || {}
    opts.credentials = 'include'
  }

  return $fetch<T>(request, {
    baseURL,
    ...opts,
    headers: customHeaders,
  })
}
