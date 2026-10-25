import { useEffect, useState } from 'react'
import { Box } from '@mui/material'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import { useNavigate, useParams } from 'react-router-dom'
import AxiosInstance from './AxiosInstance';
import FormLayout, { fila } from './FormLayout'
import MyTextField from './forms/MyTextField'
import MyMultiLineField from './forms/MyMultilineField'
import { aplicarErroresServidor } from './utils/errores'

const schema = yup.object({
  codigo_auxiliar: yup
    .string()
    .trim()
    .uppercase()
    .required('El código auxiliar es obligatorio')
    .max(30, 'Máximo 30 caracteres')
    .matches(/^[A-Z0-9_]+$/, 'Solo letras, números y guion bajo (sin espacios)'),
  nombre: yup.string().trim().required('El nombre es obligatorio').max(100, 'Máximo 100 caracteres'),
  grupo: yup.string().trim().required('El grupo es obligatorio').max(50, 'Máximo 50 caracteres'),
  descripcion: yup.string().trim().max(250, 'Máximo 250 caracteres'),
})

const valoresIniciales = { codigo_auxiliar: '', nombre: '', grupo: '', descripcion: '' }

const ConfiguracionForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [cargando, setCargando] = useState(!!id)
  const [errorGeneral, setErrorGeneral] = useState('')

  const {
    handleSubmit,
    control,
    reset,
    setError,
    formState: { isSubmitting },
  } = useForm({ defaultValues: valoresIniciales, resolver: yupResolver(schema) })

  useEffect(() => {
    if (!id) return
    AxiosInstance.get(`configuraciones/${id}/`)
      .then((res) => {
        const d = res.data
        reset({
          codigo_auxiliar: d.codigo_auxiliar,
          nombre: d.nombre,
          grupo: d.grupo,
          descripcion: d.descripcion ?? '',
        })
      })
      .catch(() => setErrorGeneral('No se pudo cargar la configuración.'))
      .finally(() => setCargando(false))
  }, [id, reset])

  const enviar = (data) => {
    const payload = {
      codigo_auxiliar: data.codigo_auxiliar,
      nombre: data.nombre,
      grupo: data.grupo,
      descripcion: data.descripcion ?? '',
    }
    setErrorGeneral('')
    const peticion = id ? AxiosInstance.patch(`configuraciones/${id}/`, payload) : AxiosInstance.post('configuraciones/', payload)
    return peticion
      .then(() => navigate('/configuraciones'))
      .catch((err) => aplicarErroresServidor(err, setError, setErrorGeneral))
  }

  if (cargando) return <p>Cargando...</p>

  return (
    <FormLayout
      titulo={id ? 'Editar configuración' : 'Nueva configuración'}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate('/configuraciones')}
    >
      <Box sx={fila}>
        <MyTextField label="Código auxiliar" name="codigo_auxiliar" control={control} placeholder="EJ_CODIGO" width="30%" />
        <MyTextField label="Nombre" name="nombre" control={control} placeholder="Nombre" width="30%" />
        <MyTextField label="Grupo" name="grupo" control={control} placeholder="Grupo" width="30%" />
      </Box>

      <Box sx={fila}>
        <MyMultiLineField label="Descripción" name="descripcion" control={control} placeholder="Descripción" width="30%" />
      </Box>
    </FormLayout>
  )
}

export default ConfiguracionForm
