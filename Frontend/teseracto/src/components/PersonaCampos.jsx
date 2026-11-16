import { useEffect, useState } from 'react'
import { Alert, Box } from '@mui/material'
import PersonIcon from '@mui/icons-material/PersonOutline'
import PlaceIcon from '@mui/icons-material/Place'
import { useWatch } from 'react-hook-form'
import * as yup from 'yup'

import AxiosInstance from './AxiosInstance'
import { Seccion } from './FormLayout'
import MyTextField from './forms/MyTextField'
import MySelectField from './forms/MySelectField'

export const TEXTO_RE = /^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]*$/
export const MSG_ESPECIALES = (nombre) =>
  `${nombre} no puede contener caracteres especiales. Use solo letras, números y espacios.`

export const grillaFormulario = {
  display: 'grid',
  gridTemplateColumns: { xs: 'minmax(0, 1fr)', sm: 'repeat(2, minmax(0, 1fr))' },
  columnGap: 3,
  rowGap: 1,
  alignItems: 'start',
  width: '100%',
  '& > *': { minWidth: 0, width: '100%' },
}

export const TIPOS_PERSONA = [
  { id: 'P', name: 'Persona natural' },
  { id: 'S', name: 'Sociedad' },
]

export const TIPOS_CUENTA = [
  { id: 'Ahorros', name: 'Ahorros' },
  { id: 'Corriente', name: 'Corriente' },
]

// ---------- Validación (misma lógica que el backend) ----------
export const personaSchema = {
  identificacion: yup
    .string()
    .trim()
    .required('La identificación es obligatoria.')
    .matches(/^(\d{10}|\d{13})$/, 'La identificación debe tener 10 o 13 dígitos.'),
  first_name: yup
    .string()
    .trim()
    .required('El nombre es obligatorio.')
    .min(2, 'El nombre debe tener al menos 2 caracteres.')
    .max(150, 'El nombre no puede superar los 150 caracteres.')
    .matches(TEXTO_RE, MSG_ESPECIALES('El nombre')),
  last_name: yup
    .string()
    .trim()
    .required('El apellido es obligatorio.')
    .min(2, 'El apellido debe tener al menos 2 caracteres.')
    .max(150, 'El apellido no puede superar los 150 caracteres.')
    .matches(TEXTO_RE, MSG_ESPECIALES('El apellido')),
  email: yup.string().trim().email('Ingresa un correo válido.'),
  telefono1: yup
    .string()
    .trim()
    .matches(/^(\d{10})?$/, 'El teléfono debe tener exactamente 10 dígitos numéricos.'),
  tipo: yup.string(),
  ubicacion: yup
    .string()
    .trim()
    .max(200, 'La ubicación no puede superar los 200 caracteres.')
    .matches(TEXTO_RE, MSG_ESPECIALES('La ubicación')),
  provincia: yup.string().nullable(), // auxiliar, no se envía
  canton: yup.string().nullable(), // auxiliar, no se envía
  localidad: yup.string().nullable(), // id de la parroquia
}

export const personaIniciales = {
  identificacion: '',
  first_name: '',
  last_name: '',
  email: '',
  telefono1: '',
  tipo: 'P',
  ubicacion: '',
  provincia: '',
  canton: '',
  localidad: '',
}

export const personaDesdeApi = (d) => ({
  identificacion: d.identificacion ?? '',
  first_name: d.first_name ?? '',
  last_name: d.last_name ?? '',
  email: d.email ?? '',
  telefono1: d.telefono1 ?? '',
  tipo: d.tipo ?? 'P',
  ubicacion: d.ubicacion ?? '',
  provincia: d.localidad_provincia ?? '',
  canton: d.localidad_canton ?? '',
  localidad: d.fk_codigo_localidad ?? '',
})

export const personaAPayload = (data) => ({
  identificacion: data.identificacion,
  first_name: data.first_name,
  last_name: data.last_name,
  email: data.email ?? '',
  telefono1: data.telefono1 ?? '',
  tipo: data.tipo || 'P',
  ubicacion: data.ubicacion ?? '',
  fk_codigo_localidad: data.localidad || null, // solo la parroquia
})

// Empresas que el usuario representa (para el select de empresa)
export const useMisEmpresas = () => {
  const [empresas, setEmpresas] = useState([])
  useEffect(() => {
    let activo = true
    AxiosInstance.get('opciones/mis_empresas/')
      .then((r) => activo && setEmpresas(r.data))
      .catch(() => activo && setEmpresas([]))
    return () => { activo = false }
  }, [])
  return empresas
}

// ---------- Componente ----------
export const PersonaCampos = ({
  control,
  setValue,
  edicion = false,
  bloqueado = false, // true = datos usados por otras empresas
  mostrarTipo = true,
}) => {
  const [provincias, setProvincias] = useState([])
  const [cantones, setCantones] = useState([])
  const [parroquias, setParroquias] = useState([])

  const provincia = useWatch({ control, name: 'provincia' })
  const canton = useWatch({ control, name: 'canton' })

  useEffect(() => {
    let activo = true
    AxiosInstance.get('opciones/localidades/', { params: { nivel: 1 } })
      .then((r) => activo && setProvincias(r.data))
      .catch(() => activo && setProvincias([]))
    return () => { activo = false }
  }, [])

  useEffect(() => {
    if (!provincia) { setCantones([]); return }
    let activo = true
    AxiosInstance.get('opciones/localidades/', { params: { nivel: 2, padre: provincia } })
      .then((r) => activo && setCantones(r.data))
      .catch(() => activo && setCantones([]))
    return () => { activo = false }
  }, [provincia])

  useEffect(() => {
    if (!canton) { setParroquias([]); return }
    let activo = true
    AxiosInstance.get('opciones/localidades/', { params: { nivel: 3, padre: canton } })
      .then((r) => activo && setParroquias(r.data))
      .catch(() => activo && setParroquias([]))
    return () => { activo = false }
  }, [canton])

  return (
    <>
      <Seccion titulo="Datos personales" icono={PersonIcon}>
        {bloqueado && (
          <Alert severity="info" sx={{ mb: 2 }}>
            Esta persona también está registrada en otras empresas, por eso sus datos
            personales no se pueden modificar desde aquí.
          </Alert>
        )}
        <Box sx={grillaFormulario}>
          <MyTextField
            label="Identificación (cédula o RUC)"
            name="identificacion"
            control={control}
            required
            disabled={edicion}
          />
          <MyTextField label="Nombres" name="first_name" control={control} required disabled={bloqueado} />
          <MyTextField label="Apellidos" name="last_name" control={control} required disabled={bloqueado} />
          <MyTextField label="Correo electrónico" name="email" control={control} disabled={bloqueado} />
          <MyTextField label="Teléfono" name="telefono1" control={control} disabled={bloqueado} />
          {mostrarTipo && (
            <MySelectField
              label="Tipo"
              name="tipo"
              control={control}
              options={TIPOS_PERSONA}
              flotante
              disabled={bloqueado}
            />
          )}
        </Box>
      </Seccion>

      <Seccion titulo="Ubicación" icono={PlaceIcon}>
        <Box sx={grillaFormulario}>
          <MySelectField
            label="Provincia"
            name="provincia"
            control={control}
            options={provincias}
            flotante
            disabled={bloqueado}
            onCambio={() => {
              setValue('canton', '')
              setValue('localidad', '')
            }}
          />
          <MySelectField
            label="Cantón"
            name="canton"
            control={control}
            options={cantones}
            flotante
            disabled={bloqueado || !provincia}
            onCambio={() => setValue('localidad', '')}
          />
          <MySelectField
            label="Parroquia"
            name="localidad"
            control={control}
            options={parroquias}
            flotante
            disabled={bloqueado || !canton}
          />
          <MyTextField label="Dirección" name="ubicacion" control={control} disabled={bloqueado} />
        </Box>
      </Seccion>
    </>
  )
}