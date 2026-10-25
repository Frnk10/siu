import Swal from 'sweetalert2'
import './alertas.css'

const Alerta = Swal.mixin({
  confirmButtonColor: '#0b66e4',
  cancelButtonColor: '#94a3b8',
  confirmButtonText: 'Aceptar',
  cancelButtonText: 'Cancelar',
  customClass: { popup: 'swal-teseracto' },
})

const Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  customClass: { popup: 'swal-teseracto-toast' },
})

export const alertaExito = (titulo, texto, opciones = {}) =>
  Alerta.fire({ icon: 'success', title: titulo, text: texto, ...opciones })

export const alertaError = (titulo, texto) =>
  Alerta.fire({ icon: 'error', title: titulo, text: texto })

export const alertaInfo = (titulo, texto) =>
  Alerta.fire({ icon: 'info', title: titulo, text: texto })

// Devuelve true si el usuario confirma
export const confirmar = async (titulo, texto, textoConfirmar = 'Sí, continuar') => {
  const r = await Alerta.fire({
    icon: 'question',
    title: titulo,
    text: texto,
    showCancelButton: true,
    confirmButtonText: textoConfirmar,
    reverseButtons: true,
  })
  return r.isConfirmed
}

// Aviso pequeño en la esquina: toast('success', 'Guardado')
export const toast = (icon, title) => Toast.fire({ icon, title })
