import { useEffect, useState } from 'react'
import { Box } from '@mui/material'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import { useNavigate, useParams } from 'react-router-dom'
import AxiosInstance from './AxiosInstance';
import FormLayout, { fila } from './FormLayout'
import MyTextField from './forms/MyTextField'
import MySelectField from './forms/MySelectField'
import { aplicarErroresServidor } from './utils/errores'

const NINGUNO = { id: '', name: '— Ninguno —' }

const schema = yup.object({
  empresa: yup.string().required('Selecciona una empresa'),
  nombre: yup
    .string()
    .trim()
    .required('El nombre es obligatorio')
    .min(2, 'Mínimo 2 caracteres')
    .max(200, 'Máximo 200 caracteres'),
  localidad: yup.string().nullable(),
  calle_principal: yup.string().trim().max(100, 'Máximo 100 caracteres'),
  calle_secundaria: yup.string().trim().max(100, 'Máximo 100 caracteres'),
})

const valoresIniciales = { empresa: '', nombre: '', localidad: '', calle_principal: '', calle_secundaria: '' }

const SucursalForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [empresas, setEmpresas] = useState([])
  const [localidades, setLocalidades] = useState([NINGUNO])
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
    const peticiones = [AxiosInstance.get('empresas/'), AxiosInstance.get('opciones/localidades/')]
    if (id) peticiones.push(AxiosInstance.get(`sucursales/${id}/`))

    Promise.all(peticiones)
      .then(([e, l, s]) => {
        setEmpresas(e.data.map((x) => ({ id: x.codigo, name: x.razon_social })))
        setLocalidades([NINGUNO, ...l.data])
        if (s) {
          const d = s.data
          reset({
            empresa: d.empresa,
            nombre: d.nombre,
            localidad: d.localidad ?? '',
            calle_principal: d.calle_principal ?? '',
            calle_secundaria: d.calle_secundaria ?? '',
          })
        }
      })
      .catch(() => setErrorGeneral('No se pudo cargar la información del formulario.'))
      .finally(() => setCargando(false))
  }, [id, reset])

  const enviar = (data) => {
    const payload = {
      empresa: data.empresa,
      nombre: data.nombre,
      localidad: data.localidad || null,
      calle_principal: data.calle_principal ?? '',
      calle_secundaria: data.calle_secundaria ?? '',
    }
    setErrorGeneral('')
    const peticion = id ? AxiosInstance.patch(`sucursales/${id}/`, payload) : AxiosInstance.post('sucursales/', payload)
    return peticion
      .then(() => navigate('/sucursales'))
      .catch((err) => aplicarErroresServidor(err, setError, setErrorGeneral))
  }

  if (cargando) return <p>Cargando...</p>

  return (
    <FormLayout
      titulo={id ? 'Editar sucursal' : 'Nueva sucursal'}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate('/sucursales')}
    >
      <Box sx={fila}>
        <MySelectField label="Empresa" name="empresa" control={control} width="30%" options={empresas} />
        <MyTextField label="Nombre de la sucursal" name="nombre" control={control} placeholder="Ej. Matriz" width="30%" />
        <MySelectField label="Localidad" name="localidad" control={control} width="30%" options={localidades} />
      </Box>

      <Box sx={fila}>
        <MyTextField label="Calle principal" name="calle_principal" control={control} placeholder="Calle principal" width="30%" />
        <MyTextField label="Calle secundaria" name="calle_secundaria" control={control} placeholder="Calle secundaria" width="30%" />
      </Box>
    </FormLayout>
  )
}

export default SucursalForm
