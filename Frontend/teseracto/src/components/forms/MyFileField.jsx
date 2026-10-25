import { Controller } from 'react-hook-form'
import { Button, FormControl, FormHelperText } from '@mui/material'

const MyFileField = ({ label, name, control, width, accept, actual }) => (
  <Controller
    name={name}
    control={control}
    render={({ field: { value, onChange }, fieldState: { error } }) => (
      <FormControl sx={{ width }} error={!!error}>
        <Button variant="outlined" component="label">
          {value?.name ?? label}
          <input
            hidden
            type="file"
            accept={accept}
            onChange={(e) => onChange(e.target.files[0] ?? null)}
          />
        </Button>
        {actual && !value && (
          <img src={actual} alt="Actual" style={{ maxHeight: 60, marginTop: 8, objectFit: 'contain' }} />
        )}
        <FormHelperText>{error?.message}</FormHelperText>
      </FormControl>
    )}
  />
)

export default MyFileField
