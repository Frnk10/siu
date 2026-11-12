import { useEffect, useState } from 'react'
import { Box, CircularProgress } from '@mui/material'
import StoreIcon from '@mui/icons-material/StorefrontOutlined'
import DescriptionIcon from '@mui/icons-material/DescriptionOutlined'
import PlaceIcon from '@mui/icons-material/Place'
import { useForm, useWatch } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import { useNavigate, useParams } from 'react-router-dom'

import AxiosInstance from './AxiosInstance'
import FormLayout, { Seccion } from './FormLayout'
import MyTextField from './forms/MyTextField'
import MySelectField from './forms/MySelectField'
import { aplicarErroresServidor } from './utils/errores'

const TEXTO_RE = /^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]*$/

const MSG_ESPECIALES = (nombre) =>
  `${nombre} no puede contener caracteres especiales. Use solo letras, números y espacios.`

const schema = yup.object({
  nombre: yup
    .string()
    .trim()
    .required('El nombre es obligatorio.')
    .min(3, 'El nombre debe tener al menos 3 caracteres.')
    .max(100, 'El nombre no puede superar los 100 caracteres.')
    .matches(TEXTO_RE, MSG_ESPECIALES('El nombre')),
  telefono: yup
    .string()
    .trim()
    .matches(/^(\d{10})?$/, 'El teléfono debe tener exactamente 10 dígitos numéricos.'),
  calle_principal: yup
    .string()
    .trim()
    .max(100, 'La calle principal no puede superar los 100 caracteres.')
    .matches(TEXTO_RE, MSG_ESPECIALES('La calle principal')),
  calle_secundaria: yup
    .string()
    .trim()
    .max(100, 'La calle secundaria no puede superar los 100 caracteres.')
    .matches(TEXTO_RE, MSG_ESPECIALES('La calle secundaria')),
  provincia: yup.string().nullable(), // auxiliar, no se envía
  canton: yup.string().nullable(), // auxiliar, no se envía
  localidad: yup.string().nullable(), // id de la parroquia
})

const valoresIniciales = {
  nombre: '',
  telefono: '',
  calle_principal: '',
  calle_secundaria: '',
  provincia: '',
  canton: '',
  localidad: '',
}

const grillaFormulario = {
  display: 'grid',
  gridTemplateColumns: { xs: 'minmax(0, 1fr)', sm: 'repeat(2, minmax(0, 1fr))' },
  columnGap: 3,
  rowGap: 1,
  alignItems: 'start',
  width: '100%',
  '& > *': { minWidth: 0, width: '100%' },
}

const SucursalForm = () => {
  const { empresaId, id } = useParams()
  const navigate = useNavigate()
  const volver = `/empresas/${empresaId}/sucursales`

  const [provincias, setProvincias] = useState([])
  const [cantones, setCantones] = useState([])
  const [parroquias, setParroquias] = useState([])
  const [cargando, setCargando] = useState(true)
  const [errorGeneral, setErrorGeneral] = useState('')

  const {
    handleSubmit,
    control,
    reset,
    setError,
    setValue,
    formState: { isSubmitting },
  } = useForm({ defaultValues: valoresIniciales, resolver: yupResolver(schema) })

  // Carga inicial
  useEffect(() => {
    let activo = true
    const peticiones = [AxiosInstance.get('opciones/localidades/', { params: { nivel: 1 } })]
    if (id) peticiones.push(AxiosInstance.get(`sucursales/${id}/`))

    Promise.all(peticiones)
      .then(([l, s]) => {
        if (!activo) return
        setProvincias(l.data)
        if (s) {
          const d = s.data
          reset({
            nombre: d.nombre ?? '',
            telefono: d.telefono ?? '',
            calle_principal: d.calle_principal ?? '',
            calle_secundaria: d.calle_secundaria ?? '',
            provincia: d.localidad_provincia ?? '',
            canton: d.localidad_canton ?? '',
            localidad: d.localidad ?? '',
          })
        }
      })
      .catch(() => {
        if (activo) setErrorGeneral('No se pudo cargar la información del formulario.')
      })
      .finally(() => {
        if (activo) setCargando(false)
      })

    return () => { activo = false }
  }, [id, reset])

  // Cascada provincia -> cantón -> parroquia
  const provincia = useWatch({ control, name: 'provincia' })
  const canton = useWatch({ control, name: 'canton' })

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

  const enviar = (data) => {
    const payload = {
      empresa: empresaId, // sale de la URL
      nombre: data.nombre,
      telefono: data.telefono ?? '',
      localidad: data.localidad || null, // solo la parroquia
      calle_principal: data.calle_principal ?? '',
      calle_secundaria: data.calle_secundaria ?? '',
    }
    setErrorGeneral('')
    const peticion = id
      ? AxiosInstance.patch(`sucursales/${id}/`, payload)
      : AxiosInstance.post('sucursales/', payload)

    return peticion
      .then(() => navigate(volver))
      .catch((err) => aplicarErroresServidor(err, setError, setErrorGeneral))
  }

  if (cargando) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 240, p: 6 }}>
        <CircularProgress />
      </Box>
    )
  }

  return (
    <FormLayout
      titulo={id ? 'Editar sucursal' : 'Nueva sucursal'}
      subtitulo={id ? 'Modifica los datos de la sucursal.' : 'Completa los datos para registrar una nueva sucursal.'}
      icono={StoreIcon}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate(volver)}
    >
      <Seccion titulo="Datos generales" icono={DescriptionIcon}>
        <Box sx={grillaFormulario}>
          <MyTextField label="Nombre de la sucursal" name="nombre" control={control} required />
          <MyTextField label="Teléfono" name="telefono" control={control} />
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
            disabled={!provincia}
            onCambio={() => setValue('localidad', '')}
          />

          <MySelectField
            label="Parroquia"
            name="localidad"
            control={control}
            options={parroquias}
            flotante
            disabled={!canton}
          />

          <MyTextField label="Calle principal" name="calle_principal" control={control} />
          <MyTextField label="Calle secundaria" name="calle_secundaria" control={control} />
        </Box>
      </Seccion>
    </FormLayout>
  )
}

export default SucursalForm
