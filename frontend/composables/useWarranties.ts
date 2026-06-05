export const useWarranties = () => {
  const { notify } = useSnackbar()
  const items = useState('items', () => new Array())
  const total = useState('total', () => 0)

  const getWarranties = async () => {
    try {
    } catch (err) {
      notify(err, 'error')
    }
  }

  return {
    items,
    total,
    getWarranties,
  }
}
