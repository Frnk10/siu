import { useEffect, useMemo, useState } from 'react'
import { Box, CircularProgress } from '@mui/material'
import CategoryIcon from '@mui/icons-material/CategoryOutlined'
import { useForm, useWatch } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import { useNavigate, useParams } from 'react-router-dom'

import AxiosInstance from './AxiosInstance'
import FormLayout from './FormLayout'
import MyTextField from './forms/MyTextField'
import MySelectField from './forms/MySelectField'
import MyMultiSelectField from './forms/MyMultiSelectField'
import { aplicarErroresServidor } from './utils/errores'

const TEXTO_RE = /^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]*$/
const NINGUNA = { id: '', name: '— Ninguna —' }

const schema = yup.object({
  nombre: yup
    .string()
    .trim()
    .required('El nombre es obligatorio.')
    .min(3, 'El nombre debe tener al menos 3 caracteres.')
    .max(100, 'El nombre no puede superar los 100 caracteres.')
    .matches(TEXTO_RE, 'El nombre no puede contener caracteres especiales. Use solo letras, números y espacios.'),
  codigo_padre: yup.mixed().nullable(),
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

const CategoriaForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const volver = '/categorias'

  const [empresas, setEmpresas] = useState([])
  const [categorias, setCategorias] = useState([])
  const [cargando, setCargando] = useState(true)
  const [errorGeneral, setErrorGeneral] = useState('')

  const {
    handleSubmit,
    control,
    reset,
    setError,
    formState: { isSubmitting },
  } = useForm({
    defaultValues: { nombre: '', codigo_padre: '', empresas: [] },
    resolver: yupResolver(schema),
  })

  const empresasSel = useWatch({ control, name: 'empresas' })

  useEffect(() => {
    let activo = true
    const peticiones = [AxiosInstance.get('opciones/mis_empresas/'), AxiosInstance.get('categorias/')]
    if (id) peticiones.push(AxiosInstance.get(`categorias/${id}/`))

    Promise.all(peticiones)
      .then(([e, lista, cat]) => {
        if (!activo) return
        setEmpresas(e.data)
        setCategorias(lista.data)
        if (cat) {
          reset({
            nombre: cat.data.nombre ?? '',
            codigo_padre: cat.data.codigo_padre ?? '',
            empresas: cat.data.empresas ?? [],
          })
        }
      })
      .catch(() => activo && setErrorGeneral('No se pudo cargar la información del formulario.'))
      .finally(() => activo && setCargando(false))

    return () => { activo = false }
  }, [id, reset])

  // Padres posibles: activos, distintos de ella misma y presentes en todas las empresas elegidas
  const padres = useMemo(() => {
    const sel = empresasSel ?? []
    return [
      NINGUNA,
      ...categorias
        .filter(
          (c) =>
            c.estado === 'A' &&
            String(c.codigo) !== String(id) &&
            sel.every((e) => (c.empresas ?? []).includes(e)),
        )
        .map((c) => ({ id: c.codigo, name: c.nombre })),
    ]
  }, [categorias, empresasSel, id])

  const enviar = (data) => {
    const payload = {
      nombre: data.nombre,
      codigo_padre: data.codigo_padre === '' ? null : data.codigo_padre,
      empresas: data.empresas,
    }
    setErrorGeneral('')
    const peticion = id
      ? AxiosInstance.patch(`categorias/${id}/`, payload)
      : AxiosInstance.post('categorias/', payload)
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
      titulo={id ? 'Editar categoría' : 'Nueva categoría'}
      subtitulo={id ? 'Modifica los datos de la categoría.' : 'Completa los datos para registrar una categoría.'}
      icono={CategoryIcon}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate(volver)}
    >
      <Box sx={grilla}>
        <MyTextField label="Nombre" name="nombre" control={control} placeholder="Nombre de la categoría" required />
        <MyMultiSelectField label="Empresas que la verán" name="empresas" control={control} options={empresas} flotante />
        <MySelectField label="Categoría padre" name="codigo_padre" control={control} options={padres} flotante />
      </Box>
    </FormLayout>
  )
}

export default CategoriaForm
