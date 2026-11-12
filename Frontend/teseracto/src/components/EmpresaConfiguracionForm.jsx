import { useEffect, useState } from 'react'
import { Box, CircularProgress } from '@mui/material'
import SettingsIcon from '@mui/icons-material/SettingsOutlined'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import { useNavigate, useParams } from 'react-router-dom'

import AxiosInstance from './AxiosInstance'
import FormLayout from './FormLayout'
import MySelectField from './forms/MySelectField'
import MyMultiLineField from './forms/MyMultilineField'
import { aplicarErroresServidor } from './utils/errores'

const schema = yup.object({
  configuracion: yup.string().required('Selecciona una configuración.'),
  valor: yup.string().trim(),
})

const valoresIniciales = { configuracion: '', valor: '' }

// Una sola columna a todo el ancho: el select y el valor miden lo mismo
const grillaFormulario = {
  display: 'grid',
  gridTemplateColumns: 'minmax(0, 1fr)',
  rowGap: 2.5,
  alignItems: 'start',
  width: '100%',
  '& > *': { minWidth: 0, width: '100%' },
}

const EmpresaConfiguracionForm = () => {
  const { empresaId, id } = useParams()
  const navigate = useNavigate()
  const volver = `/empresas/${empresaId}/configuracion`

  const [configuraciones, setConfiguraciones] = useState([])
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
    let activo = true
    const peticiones = [AxiosInstance.get('configuraciones/')]
    if (id) peticiones.push(AxiosInstance.get(`empresa_configuraciones/${id}/`))

    Promise.all(peticiones)
      .then(([c, ec]) => {
        if (!activo) return
        setConfiguraciones(
          c.data.filter((x) => x.estado === 'A').map((x) => ({ id: x.codigo, name: x.nombre })),
        )
        if (ec) {
          reset({
            configuracion: ec.data.configuracion ?? '',
            valor: ec.data.valor ?? '',
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

  const enviar = (data) => {
    const payload = {
      empresa: empresaId, // sale de la URL
      configuracion: data.configuracion,
      valor: data.valor ?? '',
    }
    setErrorGeneral('')
    const peticion = id
      ? AxiosInstance.patch(`empresa_configuraciones/${id}/`, payload)
      : AxiosInstance.post('empresa_configuraciones/', payload)

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
      titulo={id ? 'Editar configuración' : 'Agregar configuración'}
      subtitulo={
        id
          ? 'Modifica el valor de la configuración.'
          : 'Elige una configuración y define su valor para esta empresa.'
      }
      icono={SettingsIcon}
      anchoCompleto
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate(volver)}
    >
      <Box sx={grillaFormulario}>
        <MySelectField
          label="Configuración"
          name="configuracion"
          control={control}
          options={configuraciones}
          flotante
          disabled={!!id}
        />

        <MyMultiLineField
          label="Valor"
          name="valor"
          control={control}
          placeholder="Valor de la configuración"
          rows={3}
        />
      </Box>
    </FormLayout>
  )
}

export default EmpresaConfiguracionForm
