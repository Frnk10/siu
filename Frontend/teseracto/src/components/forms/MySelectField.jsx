import { FormControl, FormHelperText, InputLabel, MenuItem, Select } from '@mui/material'
import { Controller } from 'react-hook-form'

const MySelectField = ({ label, name, control, width, options = [] }) => (
  <Controller
    name={name}
    control={control}
    render={({ field, fieldState: { error } }) => (
      <FormControl variant="standard" sx={{ width }} error={!!error}>
        <InputLabel id={`${name}-label`}>{label}</InputLabel>
        <Select {...field} labelId={`${name}-label`} id={name} value={field.value ?? ''}>
          {options.map((op) => (
            <MenuItem key={op.id} value={op.id}>
              {op.name}
            </MenuItem>
          ))}
        </Select>
        <FormHelperText>{error?.message}</FormHelperText>
      </FormControl>
    )}
  />
)

export default MySelectField
