import { TextField } from '@mui/material'
import { Controller } from 'react-hook-form'

const MyMultilineField = ({ label, name, control, placeholder, width }) => (
  <Controller
    name={name}
    control={control}
    render={({ field, fieldState: { error } }) => (
      <TextField
        {...field}
        value={field.value ?? ''}
        id={name}
        label={label}
        placeholder={placeholder}
        multiline
        maxRows={4}
        fullWidth
        sx={{ width: width || '100%' }}
        error={!!error}
        helperText={error?.message}
      />
    )}
  />
)

export default MyMultilineField
