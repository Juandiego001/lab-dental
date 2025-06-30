export function $api<T>(
  request: Parameters<typeof $fetch<T>>[0],
  opts?: Parameters<typeof $fetch<T>>[1],
) {
  const csrf_access_token: any = useCookie('csrf_access_token').value || '';

  return $fetch<T>(request, {
    ...opts,
    headers: {
      'X-CSRF-TOKEN': csrf_access_token,
      ...opts?.headers,
    },
  })
}