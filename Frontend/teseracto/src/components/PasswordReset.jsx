import { useEffect, useState } from 'react'
import { Box, CircularProgress } from '@mui/material'
import { useNavigate, useParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'

import AxiosInstance from './AxiosInstance'
import AuthLayout from './auth/AuthLayout'
import EnlaceExpirado from './auth/EnlaceExpirado'
import { BotonPrimario } from './auth/AuthFields'
import MyPassField from './forms/MyPassField'
import { alertaError, alertaExito } from './utils/alertas'

const schema = yup.object({
  password: yup.string().required('Ingresa una contraseña').min(8, 'Mínimo 8 caracteres'),
  password2: yup
    .string()
    .required('Confirma tu contraseña')
    .oneOf([yup.ref('password')], 'Las contraseñas no coinciden'),
})

const PasswordReset = () => {
  const navigate = useNavigate()
  const { token } = useParams()
  const [estado, setEstado] = useState('validando') // validando | valido | expirado

  const {
    handleSubmit,
    control,
    formState: { isSubmitting },
  } = useForm({
    defaultValues: { password: '', password2: '' },
    resolver: yupResolver(schema),
  })

  // Al abrir el enlace se valida con el backend. El formulario SOLO se muestra si el
  // backend confirmó (200) que el enlace es válido; cualquier otra cosa = caducado.
  useEffect(() => {
    let activo = true
    let temporizador

    AxiosInstance.post('password_reset/validate_token/', { token })
      .then((res) => {
        if (!activo) return
        if (res?.status !== 200) {
          setEstado('expirado')
          return
        }
        setEstado('valido')
        const segundos = res.data?.segundos_restantes
        if (typeof segundos === 'number') {
          temporizador = setTimeout(() => setEstado('expirado'), segundos * 1000 + 500)
        }
      })
      .catch(() => {
        if (activo) setEstado('expirado')
      })

    return () => {
      activo = false
      clearTimeout(temporizador)
    }
  }, [token])

  const submission = (data) =>
    AxiosInstance.post('password_reset/confirm/', { password: data.password, token })
      .then((res) => {
        if (res?.status !== 200) throw new Error('Respuesta inválida')
        return alertaExito('¡Contraseña actualizada!', 'Ya puedes iniciar sesión con tu nueva contraseña.', {
          timer: 3500,
          timerProgressBar: true,
          confirmButtonText: 'Ir a iniciar sesión',
        })
      })
      .then(() => navigate('/'))
      .catch((error) => {
        // Si el enlace venció justo al enviar
        if (error.response?.status === 404) {
          setEstado('expirado')
          return
        }
        const detalle = error.response?.data?.password
        alertaError(
          'No se pudo restablecer la contraseña',
          (Array.isArray(detalle) ? detalle.join(' ') : null) || 'Inténtalo nuevamente.'
        )
      })

  if (estado === 'validando') {
    return (
      <AuthLayout titulo="Verificando enlace" subtitulo="Un momento, por favor...">
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress sx={{ color: '#0b66e4' }} />
        </Box>
      </AuthLayout>
    )
  }

  if (estado === 'expirado') return <EnlaceExpirado />

  return (
    <AuthLayout titulo="Nueva contraseña" subtitulo="Crea una contraseña segura para tu cuenta">
      <form onSubmit={handleSubmit(submission)} noValidate>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.5 }}>
          <MyPassField label="Nueva contraseña" name="password" control={control} />

          <MyPassField label="Confirmar contraseña" name="password2" control={control} />

          <BotonPrimario cargando={isSubmitting}>Restablecer contraseña</BotonPrimario>
        </Box>
      </form>
    </AuthLayout>
  )
}

export default PasswordReset