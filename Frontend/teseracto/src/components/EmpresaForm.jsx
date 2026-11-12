import { useEffect, useState } from 'react'
import { Box, CircularProgress } from '@mui/material'
import BusinessIcon from '@mui/icons-material/Business'
import DescriptionIcon from '@mui/icons-material/DescriptionOutlined'
import PlaceIcon from '@mui/icons-material/Place'
import SettingsIcon from '@mui/icons-material/Settings'
import { useForm, useWatch } from 'react-hook-form' // CAMBIO: useWatch
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import Dayjs from 'dayjs'
import { useNavigate, useParams } from 'react-router-dom'

import AxiosInstance from './AxiosInstance'
import FormLayout, { Seccion } from './FormLayout'
import MyTextField from './forms/MyTextField'
import MyDatePickerField from './forms/MyDatePickerField'
import MySelectField from './forms/MySelectField'
import MyCheckboxField from './forms/MyCheckboxField'
import MyFileField from './forms/MyFileField'
import { bordeCampo } from './forms/Campo'
import { aplicarErroresServidor } from './utils/errores'

const LOGO_MAX = 2 * 1024 * 1024
const LOGO_TIPOS = ['image/png', 'image/jpeg', 'image/webp']
const LOGO_EXTENSIONES = ['.png', '.jpg', '.jpeg', '.webp']
const FECHA_RANGO_DIAS = 3

const TEXTO_RE = /^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]*$/
const NOMBRE_ARCHIVO_RE = /^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ _-]+$/

// Prefijo para distinguir los mensajes del frontend de los del backend
const F = (msg) => ` ${msg}`

const MSG_ESPECIALES = (nombre) =>
  F(`${nombre} no puede contener caracteres especiales. Use solo letras, números y espacios.`)

const schema = yup.object({
  razon_social: yup
    .string()
    .trim()
    .required(F('La razón social es obligatoria'))
    .min(3, F('La razón social debe tener al menos 3 caracteres.'))
    .max(200, F('La razón social no puede superar los 200 caracteres.'))
    .matches(TEXTO_RE, MSG_ESPECIALES('La razón social')),
  representante: yup.string().nullable(),
  fecha_constitucion: yup
    .date()
    .nullable()
    .typeError(F('Fecha inválida'))
    .test('rango', function (v) {
      if (!v) return true
      const min = Dayjs().subtract(FECHA_RANGO_DIAS, 'day').startOf('day')
      const max = Dayjs().add(FECHA_RANGO_DIAS, 'day').endOf('day')
      const fecha = Dayjs(v)
      if (fecha.isBefore(min) || fecha.isAfter(max)) {
        return this.createError({
          message: F(
            `La fecha debe estar entre ${min.format('DD-MM-YYYY')} y ${max.format('DD-MM-YYYY')} (${FECHA_RANGO_DIAS} días antes o después de hoy).`,
          ),
        })
      }
      return true
    }),
  telefono: yup
    .string()
    .trim()
    .matches(/^(\d{10})?$/, F('El teléfono debe tener exactamente 10 dígitos numéricos.')),
  calle_principal: yup
    .string()
    .trim()
    .max(100, F('La calle principal no puede superar los 100 caracteres.'))
    .matches(TEXTO_RE, MSG_ESPECIALES('La calle principal')),
  calle_secundaria: yup
    .string()
    .trim()
    .max(100, F('La calle secundaria no puede superar los 100 caracteres.'))
    .matches(TEXTO_RE, MSG_ESPECIALES('La calle secundaria')),
  provincia: yup.string().nullable(), // NUEVO (solo auxiliar, no se envía)
  canton: yup.string().nullable(), // NUEVO (solo auxiliar, no se envía)
  localidad: yup.string().nullable(), // es el id de la parroquia
  obligado_contabilidad: yup.boolean(),
  facturacion_electronica: yup.boolean(),
  logotipo: yup
    .mixed()
    .nullable()
    .test('extension', F('El logotipo debe ser PNG, JPG o WEBP.'), (f) => {
      if (!f) return true
      const ext = f.name.slice(f.name.lastIndexOf('.')).toLowerCase()
      return LOGO_EXTENSIONES.includes(ext)
    })
    .test(
      'nombre',
      F('El nombre del archivo no puede contener caracteres especiales. Use solo letras, números, espacios, guiones (-) o guion bajo (_).'),
      (f) => {
        if (!f) return true
        const punto = f.name.lastIndexOf('.')
        const base = punto > 0 ? f.name.slice(0, punto) : f.name
        return NOMBRE_ARCHIVO_RE.test(base)
      },
    )
    .test('tamano', F('El logotipo no puede superar los 2 MB.'), (f) => !f || f.size <= LOGO_MAX)
    .test('tipo', F('El logotipo debe ser PNG, JPG o WEBP.'), (f) => !f || LOGO_TIPOS.includes(f.type)),
})

const valoresIniciales = {
  razon_social: '',
  representante: '',
  fecha_constitucion: null,
  telefono: '',
  calle_principal: '',
  calle_secundaria: '',
  provincia: '', // NUEVO
  canton: '', // NUEVO
  localidad: '',
  obligado_contabilidad: false,
  facturacion_electronica: false,
  logotipo: null,
}

const grillaFormulario = {
  display: 'grid',
  gridTemplateColumns: {
    xs: 'minmax(0, 1fr)',
    sm: 'repeat(2, minmax(0, 1fr))',
  },
  columnGap: 3,
  rowGap: 1,
  alignItems: 'start',
  width: '100%',
  '& > *': {
    minWidth: 0,
    width: '100%',
  },
}

const EmpresaForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()

  const [usuarios, setUsuarios] = useState([])
  const [provincias, setProvincias] = useState([]) // CAMBIO: antes "localidades"
  const [cantones, setCantones] = useState([]) // NUEVO
  const [parroquias, setParroquias] = useState([]) // NUEVO
  const [logoActual, setLogoActual] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [errorGeneral, setErrorGeneral] = useState('')

  const {
    handleSubmit,
    control,
    reset,
    setError,
    setValue, // NUEVO
    formState: { isSubmitting },
  } = useForm({
    defaultValues: valoresIniciales,
    resolver: yupResolver(schema),
  })

  // Carga inicial
  useEffect(() => {
    let activo = true
    const peticiones = [
      AxiosInstance.get('opciones/usuarios/'),
      AxiosInstance.get('opciones/localidades/', { params: { nivel: 1 } }), // CAMBIO: provincias
    ]
    if (id) peticiones.push(AxiosInstance.get(`empresas/${id}/`))

    Promise.all(peticiones)
      .then(([u, l, e]) => {
        if (!activo) return
        setUsuarios(u.data)
        setProvincias(l.data) // CAMBIO

        if (e) {
          const d = e.data
          setLogoActual(d.logotipo)
          reset({
            razon_social: d.razon_social ?? '',
            representante: d.representante ?? '',
            fecha_constitucion: d.fecha_constitucion ? Dayjs(d.fecha_constitucion) : null,
            telefono: d.telefono ?? '',
            calle_principal: d.calle_principal ?? '',
            calle_secundaria: d.calle_secundaria ?? '',
            provincia: d.localidad_provincia ?? '', // NUEVO
            canton: d.localidad_canton ?? '', // NUEVO
            localidad: d.localidad ?? '',
            obligado_contabilidad: d.obligado_contabilidad ?? false,
            facturacion_electronica: d.facturacion_electronica ?? false,
            logotipo: null,
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

  // NUEVO: cascada provincia -> cantón -> parroquia
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
    const fd = new FormData()
    fd.append('razon_social', data.razon_social)
    fd.append('representante', data.representante ?? '')
    fd.append('fecha_constitucion', data.fecha_constitucion ? Dayjs(data.fecha_constitucion).format('YYYY-MM-DD') : '')
    fd.append('telefono', data.telefono ?? '')
    fd.append('calle_principal', data.calle_principal ?? '')
    fd.append('calle_secundaria', data.calle_secundaria ?? '')
    fd.append('localidad', data.localidad ?? '') // solo se envía la parroquia
    fd.append('obligado_contabilidad', data.obligado_contabilidad ? 'true' : 'false')
    fd.append('facturacion_electronica', data.facturacion_electronica ? 'true' : 'false')

    if (data.logotipo instanceof File) fd.append('logotipo', data.logotipo)

    setErrorGeneral('')
    const peticion = id ? AxiosInstance.patch(`empresas/${id}/`, fd) : AxiosInstance.post('empresas/', fd)

    return peticion
      .then(() => navigate('/empresas'))
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
      titulo={id ? 'Editar empresa' : 'Nueva empresa'}
      subtitulo={id ? 'Modifica los datos de la empresa.' : 'Completa los datos para registrar una nueva empresa.'}
      icono={BusinessIcon}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate('/empresas')}
    >
      <Seccion titulo="Datos generales" icono={DescriptionIcon}>
        <Box sx={grillaFormulario}>
          <MyTextField label="Razón social" name="razon_social" control={control} required />

          <MySelectField
            label="Representante"
            name="representante"
            control={control}
            options={usuarios}
            flotante={true}
          />

          <MyDatePickerField label="Fecha de constitución" name="fecha_constitucion" control={control} />

          <MyTextField label="Teléfono" name="telefono" control={control} />
        </Box>
      </Seccion>

      {/* CAMBIO: tres selects en cascada */}
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

      <Seccion titulo="Configuración" icono={SettingsIcon}>
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: { xs: 'minmax(0, 1fr)', md: 'repeat(2, minmax(0, 1fr))' },
            gap: 2.5,
            alignItems: 'center',
            '& > *': { minWidth: 0, width: '100%' },
          }}
        >
          <MyFileField
            label="Logotipo"
            name="logotipo"
            control={control}
            accept="image/png,image/jpeg,image/webp"
            actual={logoActual}
          />

          <Box
            sx={{
              alignSelf: 'center',
              display: 'flex',
              flexDirection: 'column',
              gap: 1,
              p: 2,
              border: { xs: 'none', md: (t) => `1px solid ${bordeCampo(t)}` },
              borderRadius: 2,
            }}
          >
            <MyCheckboxField label="Obligado a llevar contabilidad" name="obligado_contabilidad" control={control} />
            <MyCheckboxField label="Facturación electrónica" name="facturacion_electronica" control={control} />
          </Box>
        </Box>
      </Seccion>
    </FormLayout>
  )
}

export default EmpresaForm
