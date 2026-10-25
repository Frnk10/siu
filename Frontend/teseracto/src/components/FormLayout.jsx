import { Alert, Box, Button, Typography } from '@mui/material'

export const fila = {
  display: 'flex',
  justifyContent: 'space-around',
  flexWrap: 'wrap',
  gap: '20px',
  marginBottom: '40px',
}

const FormLayout = ({ titulo, onSubmit, errorGeneral, enviando, onCancelar, children }) => (
  <form onSubmit={onSubmit} noValidate>
    <Box sx={{ backgroundColor: '#00003f', marginBottom: '10px', padding: '8px 20px' }}>
      <Typography sx={{ color: '#fff' }}>{titulo}</Typography>
    </Box>

    <Box sx={{ boxShadow: 3, padding: 4 }}>
      {errorGeneral && (
        <Alert severity="error" sx={{ marginBottom: '20px' }}>
          {errorGeneral}
        </Alert>
      )}

      {children}

      <Box sx={{ display: 'flex', gap: '12px' }}>
        <Button variant="contained" type="submit" disabled={enviando} sx={{ width: '30%' }}>
          Guardar
        </Button>
        <Button variant="outlined" onClick={onCancelar}>
          Cancelar
        </Button>
      </Box>
    </Box>
  </form>
)

export default FormLayout
