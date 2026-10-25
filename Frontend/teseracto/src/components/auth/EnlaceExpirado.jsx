import { useEffect, useState } from 'react'
import { Box, Link, Typography } from '@mui/material'
import { Link as RouterLink, useNavigate } from 'react-router-dom'
import LinkOff from '@mui/icons-material/LinkOff'
import AuthLayout from './AuthLayout'
import { BotonPrimario } from './AuthFields'

const SEGUNDOS = 5

// Pantalla que se muestra cuando el enlace de recuperación ya no es válido.
// Redirige sola al login después de unos segundos.
const EnlaceExpirado = () => {
  const navigate = useNavigate()
  const [restante, setRestante] = useState(SEGUNDOS)

  useEffect(() => {
    if (restante <= 0) {
      navigate('/', { replace: true })
      return
    }
    const temporizador = setTimeout(() => setRestante((r) => r - 1), 1000)
    return () => clearTimeout(temporizador)
  }, [restante, navigate])

  return (
    <AuthLayout
      titulo="Enlace caducado"
      subtitulo="Este enlace de recuperación ya no es válido o ya fue utilizado."
    >
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3 }}>
        <Box
          sx={{
            width: 88,
            height: 88,
            borderRadius: '50%',
            bgcolor: '#eaf2ff',
            color: '#0b66e4',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <LinkOff sx={{ fontSize: 44 }} />
        </Box>

        <Typography sx={{ color: '#5b6b8a', textAlign: 'center' }}>
          Serás redirigido al inicio de sesión en{' '}
          <strong style={{ color: '#0b2a6f' }}>{restante}</strong> s.
        </Typography>

        <Box sx={{ width: '100%' }}>
          <BotonPrimario type="button" onClick={() => navigate('/', { replace: true })}>
            Ir al inicio de sesión
          </BotonPrimario>
        </Box>

        <Link
          component={RouterLink}
          to="/request/password_reset"
          underline="hover"
          sx={{ color: '#0b66e4', fontWeight: 600 }}
        >
          Solicitar un nuevo enlace
        </Link>
      </Box>
    </AuthLayout>
  )
}

export default EnlaceExpirado