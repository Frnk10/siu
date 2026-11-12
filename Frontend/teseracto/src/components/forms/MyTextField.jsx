import { TextField } from '@mui/material'
import { Controller } from 'react-hook-form'
import { Campo, estiloInput } from './Campo'

const MyTextField = ({ label, name, control, placeholder, icono, required, flotante = true }) => (
  <Controller
    name={name}
    control={control}
    render={({ field, fieldState }) => (
      <Campo id={name} label={label} required={required} error={fieldState.error?.message} flotante={flotante}>
        <TextField
          {...field}
          id={name}
          value={field.value ?? ''}
          label={flotante ? label : undefined} // Si es flotante, MUI pone el label adentro
          placeholder={placeholder}
          variant="outlined"
          fullWidth
          error={!!fieldState.error}
          sx={estiloInput} // Mantiene los bordes y colores de tu proyecto
          InputProps={{
            // Si no es flotante y tiene icono, aquí se podría inyectar
          }}
        />
      </Campo>
    )}
  />
)

export default MyTextField
