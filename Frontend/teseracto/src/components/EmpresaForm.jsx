import { useEffect, useState } from 'react'
import { Box } from '@mui/material'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import Dayjs from 'dayjs'
import { useNavigate, useParams } from 'react-router-dom'
import AxiosInstance from './AxiosInstance';
import FormLayout, { fila } from './FormLayout'
import MyTextField from './forms/MyTextField'
import MyDatePickerField from './forms/MyDatePickerField'
import MySelectField from './forms/MySelectField'
import MyCheckboxField from './forms/MyCheckboxField'
import MyFileField from './forms/MyFileField'
import { aplicarErroresServidor } from './utils/errores'

const LOGO_MAX = 2 * 1024 * 1024
const LOGO_TIPOS = ['image/png', 'image/jpeg', 'image/webp']
const NINGUNO = { id: '', name: '— Ninguno —' }

const schema = yup.object({
  razon_social: yup
    .string()
    .trim()
    .required('La razón social es obligatoria')
    .min(3, 'Mínimo 3 caracteres')
    .max(200, 'Máximo 200 caracteres'),
  representante: yup.string().nullable(),
  fecha_constitucion: yup
    .date()
    .nullable()
    .typeError('Fecha inválida')
    .test('no-futura', 'La fecha no puede ser futura', (v) => !v || v <= new Date()),
  telefono: yup.string().trim().matches(/^(\+?\d{7,15})?$/, 'Teléfono inválido: de 7 a 15 dígitos'),
  calle_principal: yup.string().trim().max(100, 'Máximo 100 caracteres'),
  calle_secundaria: yup.string().trim().max(100, 'Máximo 100 caracteres'),
  localidad: yup.string().nullable(),
  obligado_contabilidad: yup.boolean(),
  facturacion_electronica: yup.boolean(),
  logotipo: yup
    .mixed()
    .nullable()
    .test('tamano', 'El logotipo no puede superar 2 MB', (f) => !f || f.size <= LOGO_MAX)
    .test('tipo', 'Solo PNG, JPG o WEBP', (f) => !f || LOGO_TIPOS.includes(f.type)),
})

const valoresIniciales = {
  razon_social: '',
  representante: '',
  fecha_constitucion: null,
  telefono: '',
  calle_principal: '',
  calle_secundaria: '',
  localidad: '',
  obligado_contabilidad: false,
  facturacion_electronica: false,
  logotipo: null,
}

const EmpresaForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [usuarios, setUsuarios] = useState([NINGUNO])
  const [localidades, setLocalidades] = useState([NINGUNO])
  const [logoActual, setLogoActual] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [errorGeneral, setErrorGeneral] = useState('')

  const {
    handleSubmit,
    control,
    reset,
    setError,
    formState: { isSubmitting },
  } = useForm({ defaultValues: valoresIniciales, resolver: yupResolver(schema) })

  useEffect(() => {
    const peticiones = [AxiosInstance.get('opciones/usuarios/'), AxiosInstance.get('opciones/localidades/')]
    if (id) peticiones.push(AxiosInstance.get(`empresas/${id}/`))

    Promise.all(peticiones)
      .then(([u, l, e]) => {
        setUsuarios([NINGUNO, ...u.data])
        setLocalidades([NINGUNO, ...l.data])
        if (e) {
          const d = e.data
          setLogoActual(d.logotipo)
          reset({
            razon_social: d.razon_social,
            representante: d.representante ?? '',
            fecha_constitucion: d.fecha_constitucion ? Dayjs(d.fecha_constitucion) : null,
            telefono: d.telefono ?? '',
            calle_principal: d.calle_principal ?? '',
            calle_secundaria: d.calle_secundaria ?? '',
            localidad: d.localidad ?? '',
            obligado_contabilidad: d.obligado_contabilidad,
            facturacion_electronica: d.facturacion_electronica,
            logotipo: null,
          })
        }
      })
      .catch(() => setErrorGeneral('No se pudo cargar la información del formulario.'))
      .finally(() => setCargando(false))
  }, [id, reset])

  const enviar = (data) => {
    const fd = new FormData()
    fd.append('razon_social', data.razon_social)
    fd.append('representante', data.representante ?? '')
    fd.append('fecha_constitucion', data.fecha_constitucion ? Dayjs(data.fecha_constitucion).format('YYYY-MM-DD') : '')
    fd.append('telefono', data.telefono ?? '')
    fd.append('calle_principal', data.calle_principal ?? '')
    fd.append('calle_secundaria', data.calle_secundaria ?? '')
    fd.append('localidad', data.localidad ?? '')
    fd.append('obligado_contabilidad', data.obligado_contabilidad ? 'true' : 'false')
    fd.append('facturacion_electronica', data.facturacion_electronica ? 'true' : 'false')
    if (data.logotipo instanceof File) fd.append('logotipo', data.logotipo)

    setErrorGeneral('')
    const peticion = id ? AxiosInstance.patch(`empresas/${id}/`, fd) : AxiosInstance.post('empresas/', fd)
    return peticion
      .then(() => navigate('/empresas'))
      .catch((err) => aplicarErroresServidor(err, setError, setErrorGeneral))
  }

  if (cargando) return <p>Cargando...</p>

  return (
    <FormLayout
      titulo={id ? 'Editar empresa' : 'Nueva empresa'}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate('/empresas')}
    >
      <Box sx={fila}>
        <MyTextField label="Razón social" name="razon_social" control={control} placeholder="Nombre de la empresa" width="30%" />
        <MyDatePickerField label="Fecha de constitución" name="fecha_constitucion" control={control} width="30%" />
        <MyTextField label="Teléfono" name="telefono" control={control} placeholder="0991234567" width="30%" />
      </Box>

      <Box sx={fila}>
        <MyTextField label="Calle principal" name="calle_principal" control={control} placeholder="Calle principal" width="30%" />
        <MyTextField label="Calle secundaria" name="calle_secundaria" control={control} placeholder="Calle secundaria" width="30%" />
        <MySelectField label="Localidad" name="localidad" control={control} width="30%" options={localidades} />
      </Box>

      <Box sx={fila}>
        <MySelectField label="Representante" name="representante" control={control} width="30%" options={usuarios} />
        <MyFileField label="Subir logotipo" name="logotipo" control={control} width="30%" accept="image/png,image/jpeg,image/webp" actual={logoActual} />
        <Box sx={{ width: '30%' }}>
          <MyCheckboxField label="Obligado a llevar contabilidad" name="obligado_contabilidad" control={control} />
          <MyCheckboxField label="Facturación electrónica" name="facturacion_electronica" control={control} />
        </Box>
      </Box>
    </FormLayout>
  )
}

export default EmpresaForm
