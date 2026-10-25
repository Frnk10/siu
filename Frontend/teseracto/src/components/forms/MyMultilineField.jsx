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
        variant="standard"
        placeholder={placeholder}
        multiline
        minRows={3}
        sx={{ width }}
        error={!!error}
        helperText={error?.message}
      />
    )}
  />
)

export default MyMultilineField
