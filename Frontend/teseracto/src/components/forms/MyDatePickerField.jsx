import Dayjs from 'dayjs'
import 'dayjs/locale/es'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker'
import { Controller } from 'react-hook-form'
import { Campo, estiloPicker } from './Campo'

const MyDatePickerField = ({ label, name, control, required }) => (
  <Controller
    name={name}
    control={control}
    render={({ field, fieldState }) => (
      <Campo id={name} label={label} required={required} error={fieldState.error?.message} flotante>
        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="es">
          <DesktopDatePicker
            label={label}
            value={field.value ? Dayjs(field.value) : null}
            onChange={(v) => field.onChange(v && v.isValid() ? v : null)}
            inputRef={field.ref}
            format="DD-MM-YYYY"
            slotProps={{
              textField: {
                id: name,
                fullWidth: true,
                error: !!fieldState.error,
                onBlur: field.onBlur,
                sx: estiloPicker,
              },
            }}
          />
        </LocalizationProvider>
      </Campo>
    )}
  />
)

export default MyDatePickerField
