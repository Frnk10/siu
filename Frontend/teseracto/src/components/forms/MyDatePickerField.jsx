import { Controller } from 'react-hook-form'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'

const MyDatePickerField = ({ label, name, control, width }) => (
  <Controller
    name={name}
    control={control}
    render={({ field: { value, onChange, onBlur }, fieldState: { error } }) => (
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DatePicker
          label={label}
          value={value ?? null}
          onChange={onChange}
          format="DD-MM-YYYY"
          slotProps={{
            textField: {
              variant: 'standard',
              onBlur,
              error: !!error,
              helperText: error?.message,
              sx: { width },
            },
          }}
        />
      </LocalizationProvider>
    )}
  />
)

export default MyDatePickerField
