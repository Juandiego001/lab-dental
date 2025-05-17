import { reactive } from 'vue'

export const createMixin = reactive({
  createDialog: true,
  show () {
    this.createDialog = true
  },
  hide () {
    this.createDialog = false
  },
  toggle () {
    this.createDialog = !this.createDialog
  }
})