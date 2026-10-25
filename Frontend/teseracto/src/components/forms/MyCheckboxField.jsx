import { Controller } from 'react-hook-form'
import { Checkbox, FormControl, FormControlLabel, FormHelperText } from '@mui/material'

const MyCheckboxField = ({ label, name, control, width }) => (
  <Controller
    name={name}
    control={control}
    render={({ field: { value, onChange }, fieldState: { error } }) => (
      <FormControl sx={{ width }} error={!!error}>
        <FormControlLabel
          control={<Checkbox checked={!!value} onChange={(e) => onChange(e.target.checked)} />}
          label={label}
        />
        <FormHelperText>{error?.message}</FormHelperText>
      </FormControl>
    )}
  />
)

export default MyCheckboxField
