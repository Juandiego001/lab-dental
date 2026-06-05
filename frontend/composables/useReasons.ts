export const useReasons = () => {
  const { notify } = useSnackbar()
  const items = useState('items', () => new Array())
  const total = useState('total', () => 0)

  const getReasons = async () => {
    try {
    } catch (err) {
      notify(err, 'error')
    }
  }

  return {
    items,
    total,
    getReasons,
  }
}
