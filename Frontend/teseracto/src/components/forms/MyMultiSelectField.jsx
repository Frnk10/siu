import { Autocomplete, Checkbox, TextField } from '@mui/material'
import { Controller } from 'react-hook-form'
import { Campo, estiloInput } from './Campo'

const TODAS = { id: '__todas__', name: 'Todas las empresas' }

const MyMultiSelectField = ({
  label,
  name,
  control,
  options = [],
  required,
  flotante = false,
  textoTodas = 'Todas las empresas',
}) => (
  <Controller
    name={name}
    control={control}
    render={({ field, fieldState }) => {
      const ids = (field.value ?? []).map(String)
      const seleccionadas = options.filter((o) => ids.includes(String(o.id)))
      const todas = options.length > 0 && seleccionadas.length === options.length
      const opciones = [{ ...TODAS, name: textoTodas }, ...options]

      const cambiar = (_, nuevas) => {
        // Si tocó "Todas": marca todas, o quita todas si ya estaban marcadas
        if (nuevas.some((o) => o.id === TODAS.id)) {
          field.onChange(todas ? [] : options.map((o) => o.id))
        } else {
          field.onChange(nuevas.map((o) => o.id))
        }
      }

      return (
        <Campo
          id={name}
          label={label}
          required={required}
          error={fieldState.error?.message}
          flotante={flotante}
        >
          <Autocomplete
            multiple
            disableCloseOnSelect
            limitTags={1}
            options={opciones}
            value={seleccionadas}
            onChange={cambiar}
            onBlur={field.onBlur}
            getOptionLabel={(o) => o?.name ?? ''}
            isOptionEqualToValue={(a, b) => String(a.id) === String(b.id)}
            noOptionsText="Sin resultados"
            clearText="Quitar selección"
            openText="Abrir"
            closeText="Cerrar"
            fullWidth
            slotProps={{ paper: { sx: { borderRadius: '10px', mt: 0.5 } } }}
            renderOption={(props, option) => {
              const { key, ...resto } = props
              const marcada = option.id === TODAS.id ? todas : ids.includes(String(option.id))
              return (
                <li key={key} {...resto}>
                  <Checkbox checked={marcada} size="small" sx={{ mr: 1, p: 0.5 }} />
                  {option.name}
                </li>
              )
            }}
            renderInput={(params) => (
              <TextField
                {...params}
                id={name}
                inputRef={field.ref}
                label={flotante ? label : undefined}
                placeholder={seleccionadas.length ? undefined : flotante ? undefined : 'Seleccionar…'}
                error={!!fieldState.error}
                sx={{
                  ...estiloInput,
                  '& .MuiOutlinedInput-root': { height: 56, py: 0 },
                  // Una sola línea: los chips sobrantes se resumen como "+2"
                  '& .MuiAutocomplete-inputRoot': { flexWrap: 'nowrap', overflow: 'hidden' },
                }}
              />
            )}
          />
        </Campo>
      )
    }}
  />
)

export default MyMultiSelectField
