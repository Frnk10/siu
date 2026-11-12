import { useEffect, useState } from 'react'
import { Box, CircularProgress } from '@mui/material'
import LocalOfferIcon from '@mui/icons-material/LocalOfferOutlined'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import { useNavigate, useParams } from 'react-router-dom'

import AxiosInstance from './AxiosInstance'
import FormLayout from './FormLayout'
import MyTextField from './forms/MyTextField'
import MyMultiSelectField from './forms/MyMultiSelectField'
import { aplicarErroresServidor } from './utils/errores'

const TEXTO_RE = /^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]*$/

const schema = yup.object({
  nombre: yup
    .string()
    .trim()
    .required('El nombre es obligatorio.')
    .min(3, 'El nombre debe tener al menos 3 caracteres.')
    .max(100, 'El nombre no puede superar los 100 caracteres.')
    .matches(TEXTO_RE, 'El nombre no puede contener caracteres especiales. Use solo letras, números y espacios.'),
  empresas: yup.array().of(yup.number()).min(1, 'Selecciona al menos una empresa.'),
})

const grilla = {
  display: 'grid',
  gridTemplateColumns: { xs: 'minmax(0, 1fr)', sm: 'repeat(2, minmax(0, 1fr))' },
  columnGap: 3,
  rowGap: 1,
  alignItems: 'start',
  width: '100%',
  '& > *': { minWidth: 0, width: '100%' },
}

const MarcaForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const volver = '/marcas'

  const [empresas, setEmpresas] = useState([])
  const [cargando, setCargando] = useState(true)
  const [errorGeneral, setErrorGeneral] = useState('')

  const {
    handleSubmit,
    control,
    reset,
    setError,
    formState: { isSubmitting },
  } = useForm({ defaultValues: { nombre: '', empresas: [] }, resolver: yupResolver(schema) })

  useEffect(() => {
    let activo = true
    const peticiones = [AxiosInstance.get('opciones/mis_empresas/')]
    if (id) peticiones.push(AxiosInstance.get(`marcas/${id}/`))

    Promise.all(peticiones)
      .then(([e, m]) => {
        if (!activo) return
        setEmpresas(e.data)
        if (m) reset({ nombre: m.data.nombre ?? '', empresas: m.data.empresas ?? [] })
      })
      .catch(() => activo && setErrorGeneral('No se pudo cargar la información del formulario.'))
      .finally(() => activo && setCargando(false))

    return () => { activo = false }
  }, [id, reset])

  const enviar = (data) => {
    const payload = { nombre: data.nombre, empresas: data.empresas }
    setErrorGeneral('')
    const peticion = id ? AxiosInstance.patch(`marcas/${id}/`, payload) : AxiosInstance.post('marcas/', payload)
    return peticion
      .then(() => navigate(volver))
      .catch((err) => aplicarErroresServidor(err, setError, setErrorGeneral))
  }

  if (cargando)
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 6 }}>
        <CircularProgress />
      </Box>
    )

  return (
    <FormLayout
      titulo={id ? 'Editar marca' : 'Nueva marca'}
      subtitulo={id ? 'Modifica los datos de la marca.' : 'Completa los datos para registrar una marca.'}
      icono={LocalOfferIcon}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate(volver)}
    >
      <Box sx={grilla}>
        <MyTextField label="Nombre" name="nombre" control={control} placeholder="Nombre de la marca" required />
        <MyMultiSelectField label="Empresas que la verán" name="empresas" control={control} options={empresas} flotante />
      </Box>
    </FormLayout>
  )
}

export default MarcaForm
