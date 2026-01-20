import { reactive } from 'vue'

export const searchMixin = reactive({
  searchDialog: false,
  show () {
    this.searchDialog = true
  },
  hide () {
    this.searchDialog = false
  },
  toggle () {
    this.searchDialog = !this.searchDialog
  }
})