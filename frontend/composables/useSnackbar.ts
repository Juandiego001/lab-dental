export const useSnackbar = () => {
  const snackbar = useState('snackbar', () => ({
    message: '',
    visible: false,
    color: 'green-darken-4'
  }))

  const show = (message: string, type: any = 'success') => {
    snackbar.value = { message, visible: true, color: type === 'success' ? 'green-darken-4' : 'red-darken-4' }
  }

  const hide = () => {
    snackbar.value.visible = false
  }

  const notify = (response: any, type: 'success' | 'error') => {
    let message = '';

    if (type === 'success') {
      if (typeof response === 'string') message = response;
      else message = response.message;
    }
    else {
      if (typeof response === 'string') message = response;
      else message = response.data.message;
    }
    show(message, type);
  }

  return {
    snackbar,
    show,
    hide,
    notify
  }
}
