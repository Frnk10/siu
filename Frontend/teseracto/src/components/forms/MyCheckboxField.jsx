import { Checkbox, FormControlLabel } from '@mui/material'
import { Controller } from 'react-hook-form'
import { colorTexto } from './Campo'

const MyCheckboxField = ({ label, name, control }) => (
  <Controller
    name={name}
    control={control}
    render={({ field }) => (
      <FormControlLabel
        label={label}
        sx={{ m: 0, '& .MuiFormControlLabel-label': { fontSize: 14.5, color: colorTexto } }}
        control={
          <Checkbox
            checked={!!field.value}
            onChange={(e) => field.onChange(e.target.checked)}
            onBlur={field.onBlur}
            inputRef={field.ref}
            sx={{ mr: 0.5, '& .MuiSvgIcon-root': { fontSize: 26 } }}
          />
        }
      />
    )}
  />
)

export default MyCheckboxField
