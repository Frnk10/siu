import { useEffect, useState } from 'react'
import { Box } from '@mui/material'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import { useNavigate, useParams } from 'react-router-dom'
import AxiosInstance from './AxiosInstance';
import FormLayout, { fila } from './FormLayout'
import MySelectField from './forms/MySelectField'
import MyMultiLineField from './forms/MyMultilineField'
import { aplicarErroresServidor } from './utils/errores'

const schema = yup.object({
  empresa: yup.string().required('Selecciona una empresa'),
  configuracion: yup.string().required('Selecciona una configuración'),
  valor: yup.string().trim(),
})

const valoresIniciales = { empresa: '', configuracion: '', valor: '' }

const EmpresaConfiguracionForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [empresas, setEmpresas] = useState([])
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
    const peticiones = [AxiosInstance.get('empresas/'), AxiosInstance.get('configuraciones/')]
    if (id) peticiones.push(AxiosInstance.get(`empresa_configuraciones/${id}/`))

    Promise.all(peticiones)
      .then(([e, c, r]) => {
        setEmpresas(e.data.map((x) => ({ id: x.codigo, name: x.razon_social })))
        setConfiguraciones(c.data.map((x) => ({ id: x.codigo, name: `${x.codigo_auxiliar} — ${x.nombre}` })))
        if (r) reset({ empresa: r.data.empresa, configuracion: r.data.configuracion, valor: r.data.valor ?? '' })
      })
      .catch(() => setErrorGeneral('No se pudo cargar la información del formulario.'))
      .finally(() => setCargando(false))
  }, [id, reset])

  const enviar = (data) => {
    const payload = { empresa: data.empresa, configuracion: data.configuracion, valor: data.valor ?? '' }
    setErrorGeneral('')
    const peticion = id
      ? AxiosInstance.patch(`empresa_configuraciones/${id}/`, payload)
      : AxiosInstance.post('empresa_configuraciones/', payload)
    return peticion
      .then(() => navigate('/empresa_configuraciones'))
      .catch((err) => aplicarErroresServidor(err, setError, setErrorGeneral))
  }

  if (cargando) return <p>Cargando...</p>

  return (
    <FormLayout
      titulo={id ? 'Editar configuración de empresa' : 'Nueva configuración de empresa'}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate('/empresa_configuraciones')}
    >
      <Box sx={fila}>
        <MySelectField label="Empresa" name="empresa" control={control} width="30%" options={empresas} />
        <MySelectField label="Configuración" name="configuracion" control={control} width="30%" options={configuraciones} />
        <MyMultiLineField label="Valor" name="valor" control={control} placeholder="Valor de la configuración" width="30%" />
      </Box>
    </FormLayout>
  )
}

export default EmpresaConfiguracionForm
