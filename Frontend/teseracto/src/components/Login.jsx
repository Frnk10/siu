import { Box, Link } from '@mui/material'
import { Link as RouterLink, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import ArrowForward from '@mui/icons-material/ArrowForward'

import AxiosInstance from './AxiosInstance'
import AuthLayout from './auth/AuthLayout'
import { BotonPrimario } from './auth/AuthFields'
import MyTextField from './forms/MyTextField'
import MyPassField from './forms/MyPassField'
import { alertaError, toast } from './utils/alertas'

const schema = yup.object({
  email: yup.string().required('Ingresa tu correo electrónico').email('Correo electrónico inválido'),
  password: yup.string().required('Ingresa tu contraseña'),
})

const Login = () => {
  const navigate = useNavigate()
  const {
    handleSubmit,
    control,
    formState: { isSubmitting },
  } = useForm({
    defaultValues: { email: '', password: '' },
    resolver: yupResolver(schema),
  })

  const submission = (data) =>
    AxiosInstance.post('login/', {
      email: data.email.trim(),
      password: data.password,
    })
      .then((response) => {
        localStorage.setItem('Token', response.data.token)
        toast('success', 'Bienvenido')
        navigate('/home')
      })
      .catch((error) => {
        const limitado = error.response?.status === 429
        alertaError(
          limitado ? 'Demasiados intentos' : 'No se pudo iniciar sesión',
          limitado
            ? 'Espera unos minutos antes de intentarlo nuevamente.'
            : 'Verifica tu correo electrónico y contraseña, e inténtalo nuevamente.'
        )
      })

  return (
    <AuthLayout titulo="Iniciar sesión" subtitulo="Accede a tu cuenta para continuar">
      <form onSubmit={handleSubmit(submission)} noValidate>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.5 }}>
          <MyTextField label="Correo electrónico" name="email" control={control} />

          <MyPassField label="Contraseña" name="password" control={control} />

          <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
            <Link
              component={RouterLink}
              to="/request/password_reset"
              underline="hover"
              sx={{ color: '#0b66e4', fontWeight: 600, fontSize: '.9rem' }}
            >
              ¿Olvidaste tu contraseña?
            </Link>
          </Box>

          <BotonPrimario cargando={isSubmitting} icono={<ArrowForward />}>
            Iniciar sesión
          </BotonPrimario>
        </Box>
      </form>
    </AuthLayout>
  )
}

export default Login