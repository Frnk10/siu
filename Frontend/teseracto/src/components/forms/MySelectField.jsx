import { Autocomplete, TextField } from '@mui/material'
import { Controller } from 'react-hook-form'
import { Campo, estiloInput } from './Campo'

const MySelectField = ({ label, name, control, options = [], required, flotante = false }) => (
  <Controller
    name={name}
    control={control}
    render={({ field, fieldState }) => {
      // El formulario guarda solo el id; aquí se busca la opción completa
      const seleccionado =
        options.find((o) => String(o.id) === String(field.value ?? '')) ?? null

      return (
        <Campo
          id={name}
          label={label}
          required={required}
          error={fieldState.error?.message}
          flotante={flotante}
        >
          <Autocomplete
            options={options}
            value={seleccionado}
            onChange={(_, nuevo) => field.onChange(nuevo ? nuevo.id : '')}
            onBlur={field.onBlur}
            getOptionLabel={(o) => o?.name ?? ''}
            isOptionEqualToValue={(a, b) => a.id === b.id}
            noOptionsText="Sin resultados"
            clearText="Quitar selección"
            openText="Abrir"
            closeText="Cerrar"
            fullWidth
            slotProps={{ paper: { sx: { borderRadius: '10px', mt: 0.5 } } }}
            renderInput={(params) => (
              <TextField
                {...params}
                id={name}
                inputRef={field.ref}
                label={flotante ? label : undefined}
                placeholder={flotante ? undefined : 'Buscar…'}
                error={!!fieldState.error}
                sx={{
                  ...estiloInput,
                  '& .MuiOutlinedInput-root': { height: 56, py: 0 },
                }}
              />
            )}
          />
        </Campo>
      )
    }}
  />
)

export default MySelectField
