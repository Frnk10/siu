
import TextField from '@mui/material/TextField';
import { Controller } from 'react-hook-form';

export default function MyTextField({ label, name, control }) {
  return (
    <Controller
      name={name}
      control={control}
      defaultValue=""
      render={({ field, fieldState: { error } }) => (
        <TextField
          {...field}
          id={name}
          value={field.value ?? ''}
          label={label}
          variant="outlined"
          className="myForm"
          error={!!error}
          helperText={error?.message}
          fullWidth
        />
      )}
    />
  );
}
