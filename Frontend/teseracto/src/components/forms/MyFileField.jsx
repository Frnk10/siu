import { useEffect, useRef, useState } from 'react'
import { Box, Button, Typography } from '@mui/material'
import { alpha } from '@mui/material/styles'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'
import { Controller } from 'react-hook-form'
import { Campo, bordeCampo, colorTexto } from './Campo'

const Zona = ({ id, value, onChange, accept, actual, error }) => {
  const ref = useRef(null)
  const [arrastrando, setArrastrando] = useState(false)
  const [preview, setPreview] = useState(null)

  useEffect(() => {
    if (value instanceof File) {
      const url = URL.createObjectURL(value)
      setPreview(url)
      return () => URL.revokeObjectURL(url)
    }
    setPreview(null)
  }, [value])

  const src = preview || actual
  const abrir = () => ref.current?.click()
  const quitar = (e) => {
    e.stopPropagation()
    if (ref.current) ref.current.value = ''
    onChange(null)
  }

  return (
    <Box
      role="button"
      tabIndex={0}
      onClick={abrir}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && (e.preventDefault(), abrir())}
      onDragOver={(e) => {
        e.preventDefault()
        setArrastrando(true)
      }}
      onDragLeave={() => setArrastrando(false)}
      onDrop={(e) => {
        e.preventDefault()
        setArrastrando(false)
        const f = e.dataTransfer.files?.[0]
        if (f) onChange(f)
      }}
      sx={{
        height: 112,
        borderRadius: '10px',
        border: '1.5px dashed',
        borderColor: error ? 'error.main' : arrastrando ? 'primary.main' : bordeCampo,
        bgcolor: (t) => alpha(t.palette.primary.main, arrastrando ? 0.1 : 0.04),
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 2,
        px: 2,
        transition: 'background-color .15s, border-color .15s',
        '&:hover': { bgcolor: (t) => alpha(t.palette.primary.main, 0.08) },
        '&:focus-visible': { outline: '2px solid', outlineColor: 'primary.main', outlineOffset: 2 },
      }}
    >
      <input
        ref={ref}
        id={id}
        type="file"
        accept={accept}
        hidden
        onChange={(e) => {
          const file = e.target.files?.[0]
          if (file) onChange(file) // Aseguramos que se envíe el File real
        }}
      />

      {src ? (
        <>
          <Box
            component="img"
            src={src}
            alt="Logotipo"
            sx={{ width: 72, height: 72, objectFit: 'contain', borderRadius: '8px', bgcolor: '#fff', border: (t) => `1px solid ${bordeCampo(t)}` }}
          />
          <Box sx={{ minWidth: 0 }}>
            <Typography noWrap sx={{ fontSize: 14, fontWeight: 600, color: colorTexto, maxWidth: 220 }}>
              {/* Quitamos el texto duplicado, mostramos el nombre del archivo */}
              {value instanceof File ? value.name : 'Logotipo actual'}
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
              <Button size="small" sx={{ textTransform: 'none', p: 0, minWidth: 0 }}>
                Cambiar
              </Button>
              {value instanceof File && (
                <Button size="small" color="error" onClick={quitar} sx={{ textTransform: 'none', p: 0, minWidth: 0 }}>
                  Quitar
                </Button>
              )}
            </Box>
          </Box>
        </>
      ) : (
        <Box sx={{ textAlign: 'center' }}>
          <CloudUploadIcon sx={{ color: 'primary.main', fontSize: 32 }} />
          <Typography sx={{ color: 'primary.main', fontSize: 14, fontWeight: 600 }}>
            Selecciona o arrastra un archivo
          </Typography>
          <Typography sx={{ color: 'text.secondary', fontSize: 12 }}>PNG, JPG o WEBP (máx. 2 MB)</Typography>
        </Box>
      )}
    </Box>
  )
}

const MyFileField = ({ label, name, control, accept, actual, required }) => (
  <Controller
    name={name}
    control={control}
    render={({ field, fieldState }) => (
      <Campo id={name} label={label} required={required} error={fieldState.error?.message} flotante={true}>
        <Zona
          id={name}
          value={field.value}
          onChange={field.onChange}
          accept={accept}
          actual={actual}
          error={!!fieldState.error}
        />
      </Campo>
    )}
  />
)

export default MyFileField
