import { createTheme } from '@mui/material/styles'

export const colores = {
  primary: '#1976d2',
  secondary: '#9c27b0',
  background: '#f5f5f5',
}

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: colores.primary,
    },
    secondary: {
      main: colores.secondary,
    },
    background: {
      default: colores.background,
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
})

export default theme