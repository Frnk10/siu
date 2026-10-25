import { useState } from 'react'
import { Controller } from 'react-hook-form'
import { Button, CircularProgress, IconButton, InputAdornment, TextField } from '@mui/material'
import Visibility from '@mui/icons-material/Visibility'
import VisibilityOff from '@mui/icons-material/VisibilityOff'

const estiloInput = {
  '& .MuiOutlinedInput-root': {
    borderRadius: '12px',
    bgcolor: '#fff',
    '& fieldset': { borderColor: '#cfdcf0' },
    '&:hover fieldset': { borderColor: '#8db8f8' },
    '&.Mui-focused fieldset': { borderColor: '#0b66e4', borderWidth: '2px' },
  },
  '& .MuiInputBase-input': { py: '17px' },
}

export const CampoTexto = ({ name, control, label, icono, rules, type = 'text', autoComplete }) => (
  <Controller
    name={name}
    control={control}
    rules={rules}
    render={({ field, fieldState: { error } }) => (
      <TextField
        {...field}
        value={field.value ?? ''}
        type={type}
        fullWidth
        placeholder={label}
        autoComplete={autoComplete}
        error={!!error}
        helperText={error?.message}
        sx={estiloInput}
        inputProps={{ 'aria-label': label }}
        InputProps={{
          startAdornment: icono ? (
            <InputAdornment position="start" sx={{ color: '#5b6b8a' }}>
              {icono}
            </InputAdornment>
          ) : null,
        }}
      />
    )}
  />
)

export const CampoClave = ({ name, control, label, icono, rules, autoComplete }) => {
  const [visible, setVisible] = useState(false)

  return (
    <Controller
      name={name}
      control={control}
      rules={rules}
      render={({ field, fieldState: { error } }) => (
        <TextField
          {...field}
          value={field.value ?? ''}
          type={visible ? 'text' : 'password'}
          fullWidth
          placeholder={label}
          autoComplete={autoComplete}
          error={!!error}
          helperText={error?.message}
          sx={estiloInput}
          inputProps={{ 'aria-label': label }}
          InputProps={{
            startAdornment: icono ? (
              <InputAdornment position="start" sx={{ color: '#5b6b8a' }}>
                {icono}
              </InputAdornment>
            ) : null,
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  onClick={() => setVisible((v) => !v)}
                  edge="end"
                  aria-label={visible ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                  sx={{ color: '#5b6b8a' }}
                >
                  {visible ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      )}
    />
  )
}

export const BotonPrimario = ({ children, cargando = false, icono, ...props }) => (
  <Button
    type="submit"
    variant="contained"
    fullWidth
    disabled={cargando}
    endIcon={cargando ? null : icono}
    sx={{
      py: 1.7,
      borderRadius: '12px',
      textTransform: 'none',
      fontSize: '1rem',
      fontWeight: 700,
      bgcolor: '#0b66e4',
      boxShadow: '0 8px 18px rgba(11,102,228,.28)',
      '&:hover': { bgcolor: '#0956c4', boxShadow: '0 8px 18px rgba(11,102,228,.36)' },
    }}
    {...props}
  >
    {cargando ? <CircularProgress size={22} color="inherit" /> : children}
  </Button>
)
