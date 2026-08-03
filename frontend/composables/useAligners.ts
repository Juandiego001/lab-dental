export const useAligners = () => {
  const { notify } = useSnackbar()
  const alignerData = useState('alignerData', () => ({}))
  const viewAligner = useState('viewAligner', () => false)
  const serialNumber = useState('serialNumber', () => '')
  const semantic = useState('alignerSemantic', () => undefined)
  const path = useState('alignerPath', () => undefined)

  const getAligner = async () => {
    try {
      const data = await $api<any>(`/api/aligners/${serialNumber.value}`, {
        method: 'GET',
      })
      alignerData.value = data
      viewAligner.value = true
    } catch (err) {
      notify(err, 'error')
    }
  }

  const getLastVersion = async () => {
    try {
      const data = await $api<any>('/api/aligners/utils/version', {
        method: 'GET',
      })
      semantic.value = data.semantic
      path.value = data.path
    } catch (err) {
      notify(err, 'error')
    }
  }

  const sendStage = async () => {
    try {
      const { message } = await $api<any>(
        `/api/aligners/stage/${serialNumber.value}`,
        { method: 'POST' },
      )
      return message
    } catch (err) {
      notify(err, 'error')
    }
  }

  const sendUnstage = async () => {
    try {
      const { message } = await $api<any>(
        `/api/aligners/unstage/${serialNumber.value}`,
        { method: 'POST' },
      )
      return message
    } catch (err) {
      notify(err, 'error')
    }
  }

  const sendCloud = async () => {
    try {
      const { message } = await $api<any>(
        `/api/aligners/cloud/${serialNumber.value}`,
        { method: 'POST' },
      )
      notify(message, 'success')
    } catch (err) {
      notify(err, 'error')
    }
  }

  const sendActivate = async () => {
    try {
      const { message } = await $api<any>(
        `/api/aligners/activate/${serialNumber.value}`,
        { method: 'POST' },
      )
    } catch (err) {
      notify(err, 'error')
    }
  }

  return {
    getAligner,
    alignerData,
    viewAligner,
    getLastVersion,
    sendStage,
    serialNumber,
    sendUnstage,
    sendCloud,
    semantic,
    path,
    sendActivate,
  }
}
