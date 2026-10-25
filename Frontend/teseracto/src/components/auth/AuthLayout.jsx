import { Box, Typography } from '@mui/material'
import { IlustracionLaptop, LogoTeseracto } from './Ilustraciones'

const FONDO_AZUL = 'linear-gradient(160deg, #2a85f2 0%, #0b5bd8 55%, #0a4fc0 100%)'

// Pantalla dividida: panel de marca (azul) + formulario (blanco).
const AuthLayout = ({ titulo, subtitulo, children }) => (
  <Box
    sx={{
      position: 'fixed',
      inset: 0,
      overflowY: 'auto',
      bgcolor: '#fff',
      display: 'grid',
      gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
      textAlign: 'left',
    }}
  >
    {/* Panel de marca (solo en pantallas medianas y grandes) */}
    <Box
      sx={{
        display: { xs: 'none', md: 'flex' },
        flexDirection: 'column',
        justifyContent: 'center',
        gap: 3,
        p: { md: 6, lg: 10 },
        color: '#fff',
        background: FONDO_AZUL,
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <Box
        sx={{
          position: 'absolute',
          width: 560,
          height: 560,
          borderRadius: '50%',
          bgcolor: 'rgba(255,255,255,.06)',
          bottom: -300,
          left: -180,
        }}
      />
      <Box sx={{ position: 'relative', display: 'flex', alignItems: 'center', gap: 2 }}>
        <LogoTeseracto size={64} />
        <Typography sx={{ fontSize: '2.8rem', fontWeight: 700, letterSpacing: '-1px' }}>Teseracto</Typography>
      </Box>
      <Typography sx={{ position: 'relative', fontSize: '1.3rem', maxWidth: 300, lineHeight: 1.4 }}>
        Tu sistema, más simple, más eficiente.
      </Typography>
      <Box sx={{ position: 'relative', mt: 2 }}>
        <IlustracionLaptop />
      </Box>
    </Box>

    {/* Formulario */}
    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', p: { xs: 3, sm: 6 } }}>
      <Box sx={{ width: '100%', maxWidth: 440 }}>
        {/* Logo compacto para móviles */}
        <Box sx={{ display: { xs: 'flex', md: 'none' }, alignItems: 'center', gap: 1.5, mb: 4 }}>
          <LogoTeseracto size={40} variante="azul" />
          <Typography sx={{ fontSize: '1.6rem', fontWeight: 700, color: '#0b66e4' }}>Teseracto</Typography>
        </Box>

        <Typography component="h1" sx={{ fontSize: '2.1rem', fontWeight: 800, color: '#0b2a6f', lineHeight: 1.2 }}>
          {titulo}
        </Typography>
        <Typography sx={{ color: '#5b6b8a', mt: 1, mb: 4 }}>{subtitulo}</Typography>

        {children}
      </Box>
    </Box>
  </Box>
)

export default AuthLayout
