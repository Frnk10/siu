import { Box, Link } from '@mui/material'
import { Link as RouterLink, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import EmailOutlined from '@mui/icons-material/EmailOutlined'
import ArrowBack from '@mui/icons-material/ArrowBack'

import AxiosInstance from './AxiosInstance'
import AuthLayout from './auth/AuthLayout'
import { BotonPrimario } from './auth/AuthFields'
import MyTextField from './forms/MyTextField'
import { alertaError, alertaExito } from './utils/alertas'

const PasswordResetRequest = () => {
  const navigate = useNavigate()
  const {
    handleSubmit,
    control,
    formState: { isSubmitting },
  } = useForm({ defaultValues: { email: '' } })

  const submission = async (data) => {
    try {
      await AxiosInstance.post('password_reset/', { email: data.email.trim() })
      await alertaExito(
        'Revisa tu correo',
        'Si el correo existe, recibirás instrucciones para restablecer tu contraseña.'
      )
      navigate('/')
    } catch (error) {
      alertaError(
        error.response?.status === 429 ? 'Demasiadas solicitudes' : 'No se pudo procesar la solicitud',
        error.response?.status === 429
          ? 'Espera antes de intentarlo nuevamente.'
          : 'Inténtalo nuevamente en unos minutos.'
      )
    }
  }

  return (
    <AuthLayout
      titulo="Recuperar contraseña"
      subtitulo="Ingresa tu correo y te enviaremos un enlace para crear una nueva contraseña"
    >
      <form onSubmit={handleSubmit(submission)} noValidate>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.5 }}>
          <MyTextField
            name="email"
            control={control}
            label="Correo electrónico"
            autoComplete="email"
            icono={<EmailOutlined />}
            rules={{
              required: 'Ingresa tu correo electrónico',
              pattern: { value: /^\S+@\S+\.\S+$/, message: 'Correo electrónico inválido' },
            }}
          />

          <BotonPrimario cargando={isSubmitting}>Solicitar recuperación</BotonPrimario>

          <Link
            component={RouterLink}
            to="/"
            underline="hover"
            sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5, color: '#0b66e4', fontWeight: 600 }}
          >
            <ArrowBack fontSize="small" /> Volver al inicio de sesión
          </Link>
        </Box>
      </form>
    </AuthLayout>
  )
}

export default PasswordResetRequest