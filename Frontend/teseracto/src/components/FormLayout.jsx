import { Alert, Box, Button, CircularProgress, Typography } from '@mui/material'
import { alpha, darken, lighten } from '@mui/material/styles'
import DescriptionIcon from '@mui/icons-material/DescriptionOutlined'
import SaveIcon from '@mui/icons-material/Save'

const navy = (t) => darken(t.palette.primary.main, 0.45)
const lineaSuave = (t) => `1px solid ${lighten(t.palette.primary.main, 0.88)}`

// Fila flexible (compatibilidad con formularios anteriores)
export const fila = { display: 'flex', flexWrap: 'wrap', gap: 2, mb: 2 }

// Grilla de 2 columnas (1 en móvil). Cada campo reserva su línea de error,
// por eso el espacio entre filas es pequeño.
export const grilla = {
  display: 'grid',
  gridTemplateColumns: { xs: 'minmax(0, 1fr)', md: 'repeat(2, minmax(0, 1fr))' },
  columnGap: 3,
  rowGap: 0.5,
  alignItems: 'start',
}

// Para que un campo ocupe todo el ancho de la grilla
export const anchoCompleto = { gridColumn: { md: '1 / -1' } }

// Sección: tarjeta con cabecera azul claro e ícono en círculo
export const Seccion = ({ titulo, icono: Icono, children }) => (
  <Box
    sx={{
      mb: 3,
      borderRadius: '12px',
      border: lineaSuave,
      overflow: 'hidden',
      bgcolor: '#fff',
      boxShadow: (t) => `0 1px 6px ${alpha(t.palette.primary.main, 0.06)}`,
    }}
  >
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        gap: 1.5,
        px: 2,
        py: 1.25,
        bgcolor: (t) => lighten(t.palette.primary.main, 0.92),
      }}
    >
      {Icono && (
        <Box
          sx={{
            width: 32,
            height: 32,
            borderRadius: '50%',
            display: 'grid',
            placeItems: 'center',
            color: '#fff',
            bgcolor: 'primary.main',
          }}
        >
          <Icono sx={{ fontSize: 18 }} />
        </Box>
      )}
      <Typography sx={{ fontWeight: 700, fontSize: 17, color: 'primary.main' }}>{titulo}</Typography>
    </Box>
    <Box sx={{ p: { xs: 2, sm: 3 }, pb: { xs: 1.5, sm: 2 } }}>{children}</Box>
  </Box>
)

const FormLayout = ({
  titulo,
  subtitulo,
  icono: Icono = DescriptionIcon,
  onSubmit,
  errorGeneral,
  enviando,
  onCancelar,
  textoGuardar = 'Guardar',
  children,
}) => (
  <Box
    component="form"
    onSubmit={onSubmit}
    noValidate
    sx={{
      maxWidth: 900,
      mx: 'auto',
      bgcolor: '#fff',
      borderRadius: 4,
      p: { xs: 2, sm: 3 },
      boxShadow: (t) => `0 2px 16px ${alpha(t.palette.primary.main, 0.1)}`,
    }}
  >
    {/* Encabezado */}
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, pb: 2.5, mb: 3, borderBottom: lineaSuave }}>
      <Box
        sx={{
          width: 56,
          height: 56,
          flexShrink: 0,
          borderRadius: '50%',
          display: 'grid',
          placeItems: 'center',
          color: '#fff',
          bgcolor: 'primary.main',
        }}
      >
        <Icono sx={{ fontSize: 28 }} />
      </Box>
      <Box>
        <Typography variant="h5" sx={{ fontWeight: 800, color: navy, lineHeight: 1.2 }}>
          {titulo}
        </Typography>
        {subtitulo && (
          <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.25 }}>
            {subtitulo}
          </Typography>
        )}
      </Box>
    </Box>

    {errorGeneral && (
      <Alert severity="error" sx={{ mb: 3 }}>
        {errorGeneral}
      </Alert>
    )}

    {children}

    {/* Botones */}
    <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1.5, pt: 2.5, borderTop: lineaSuave }}>
      <Button
        type="button"
        variant="outlined"
        onClick={onCancelar}
        disabled={enviando}
        sx={{ borderRadius: '10px', px: 3, height: 44, textTransform: 'none', fontWeight: 700 }}
      >
        Cancelar
      </Button>
      <Button
        type="submit"
        variant="contained"
        disabled={enviando}
        startIcon={enviando ? <CircularProgress size={16} color="inherit" /> : <SaveIcon />}
        sx={{ borderRadius: '10px', px: 3.5, height: 44, textTransform: 'none', fontWeight: 700, boxShadow: 'none' }}
      >
        {enviando ? 'Guardando…' : textoGuardar}
      </Button>
    </Box>
  </Box>
)

export default FormLayout
