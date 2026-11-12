import { Box, FormHelperText, InputAdornment } from '@mui/material'
import { darken, lighten } from '@mui/material/styles'

export const colorTexto = (t) => darken(t.palette.primary.main, 0.45)
export const bordeCampo = (t) => lighten(t.palette.primary.main, 0.7)

// Selectores del contorno (inputs normales y del DatePicker de MUI X)
const contorno = (pre) =>
  ['MuiOutlinedInput', 'MuiPickersOutlinedInput'].map((v) => `${pre}.${v}-notchedOutline`).join(', ')

// Estilo común de todos los inputs: mismo alto (56 px) y mismas esquinas
export const estiloInput = {
  borderRadius: '10px',
  backgroundColor: '#fff',
  fontSize: 15,
  height: 56,
  [contorno('& ')]: { borderColor: bordeCampo },
  [contorno('&:hover ')]: { borderColor: (t) => t.palette.primary.light },
  [contorno('&.Mui-focused ')]: { borderColor: 'primary.main', borderWidth: 1.5 },
  [contorno('&.Mui-error ')]: { borderColor: 'error.main' },
  '& input::placeholder': { color: 'text.disabled', opacity: 1 },
}

// Para el DatePicker (el estilo va sobre su raíz)
export const estiloPicker = {
  '& .MuiOutlinedInput-root, & .MuiPickersOutlinedInput-root': estiloInput,
}

// Ícono + separador vertical al inicio del campo
export const Prefijo = ({ icono: Icono }) => (
  <InputAdornment position="start" sx={{ mr: 1.5 }}>
    <Icono sx={{ color: 'text.secondary', fontSize: 22 }} />
    <Box sx={{ width: '1px', height: 24, ml: 1.5, bgcolor: bordeCampo }} />
  </InputAdornment>
)

// Misma altura que ocupa la etiqueta de arriba (14px * 1.3 + 6px)
const ALTO_ETIQUETA = 'calc(14px * 1.3 + 6px)'

// Etiqueta arriba + campo + línea reservada para el error.
// Con `flotante`, no se dibuja la etiqueta de arriba (la pone el propio campo
// dentro del borde) pero se deja el espacio para que todo siga alineado.
export const Campo = ({ id, label, required, error, flotante, children, sx }) => (
  <Box sx={{ display: 'flex', flexDirection: 'column', minWidth: 0, ...sx }}>
    {flotante ? (
      <Box aria-hidden sx={{ height: ALTO_ETIQUETA }} />
    ) : (
      <Box
        component="label"
        htmlFor={id}
        sx={{ fontWeight: 700, fontSize: 14, color: colorTexto, mb: 0.75, lineHeight: 1.3 }}
      >
        {label}
        {required && (
          <Box component="span" sx={{ color: 'error.main', ml: 0.5 }}>
            *
          </Box>
        )}
      </Box>
    )}
    {children}
    <FormHelperText error sx={{ mx: 0.5, mt: 0.5, minHeight: 20 }}>
      {error || ' '}
    </FormHelperText>
  </Box>
)