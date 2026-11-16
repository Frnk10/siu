import { useEffect, useMemo, useState } from 'react'
import { Box, CircularProgress } from '@mui/material'
import PeopleIcon from '@mui/icons-material/PeopleAltOutlined'
import CreditCardIcon from '@mui/icons-material/CreditCardOutlined'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import { useNavigate, useParams } from 'react-router-dom'

import AxiosInstance from './AxiosInstance'
import FormLayout, { Seccion } from './FormLayout'
import MyTextField from './forms/MyTextField'
import MyMultiSelectField from './forms/MyMultiSelectField'
import { aplicarErroresServidor } from './utils/errores'
import {
  PersonaCampos, personaSchema, personaIniciales, personaDesdeApi, personaAPayload,
  useMisEmpresas, grillaFormulario, TEXTO_RE, MSG_ESPECIALES,
} from './PersonaCampos'

const numero = () =>
  yup.number().transform((v, o) => (o === '' ? 0 : v)).typeError('Ingresa un número válido.')

const crearSchema = (esEdicion) =>
  yup.object({
    ...personaSchema,
    empresa_nombre: yup.string().nullable(), // solo se muestra al editar
    empresas: esEdicion
      ? yup.array()
      : yup.array().of(yup.number()).min(1, 'Selecciona al menos una empresa.'),
    limite_credito: numero()
      .min(0, 'El límite no puede ser negativo.')
      .max(9999999999.99, 'El límite es demasiado alto.'),
    dias_credito: numero()
      .integer('Los días deben ser un número entero.')
      .min(0, 'Los días no pueden ser negativos.'),
    observaciones: yup.string().trim().matches(TEXTO_RE, MSG_ESPECIALES('Las observaciones')),
  })

const valoresIniciales = {
  ...personaIniciales,
  empresas: [],
  empresa_nombre: '',
  limite_credito: 0,
  dias_credito: 0,
  observaciones: '',
}

const ClienteForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const volver = '/clientes'
  const empresas = useMisEmpresas()
  const schema = useMemo(() => crearSchema(!!id), [id])

  const [cargando, setCargando] = useState(!!id)
  const [compartido, setCompartido] = useState(false)
  const [errorGeneral, setErrorGeneral] = useState('')

  const {
    handleSubmit, control, reset, setError, setValue,
    formState: { isSubmitting },
  } = useForm({ defaultValues: valoresIniciales, resolver: yupResolver(schema) })

  useEffect(() => {
    if (!id) return
    let activo = true
    AxiosInstance.get(`clientes/${id}/`)
      .then((r) => {
        if (!activo) return
        const d = r.data
        setCompartido(!!d.datos_compartidos)
        reset({
          ...personaDesdeApi(d),
          empresas: [],
          empresa_nombre: d.empresa_nombre ?? '',
          limite_credito: d.limite_credito ?? 0,
          dias_credito: d.dias_credito ?? 0,
          observaciones: d.observaciones ?? '',
        })
      })
      .catch(() => activo && setErrorGeneral('No se pudo cargar la información del cliente.'))
      .finally(() => activo && setCargando(false))
    return () => { activo = false }
  }, [id, reset])

  // Si solo representa una empresa, se selecciona sola
  useEffect(() => {
    if (!id && empresas.length === 1) setValue('empresas', [empresas[0].id])
  }, [id, empresas, setValue])

  const enviar = (data) => {
    const payload = {
      ...personaAPayload(data),
      limite_credito: data.limite_credito,
      dias_credito: data.dias_credito,
      observaciones: data.observaciones ?? '',
    }
    if (!id) payload.empresas = data.empresas

    setErrorGeneral('')
    const peticion = id
      ? AxiosInstance.patch(`clientes/${id}/`, payload)
      : AxiosInstance.post('clientes/', payload)

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
      titulo={id ? 'Editar cliente' : 'Nuevo cliente'}
      subtitulo={
        id
          ? 'Modifica los datos del cliente en esta empresa.'
          : 'Puedes vincularlo a varias empresas a la vez. Si la identificación ya existe, se reutilizan sus datos.'
      }
      icono={PeopleIcon}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate(volver)}
    >
      <PersonaCampos control={control} setValue={setValue} edicion={!!id} bloqueado={compartido} />

      <Seccion titulo="Datos comerciales" icono={CreditCardIcon}>
        <Box sx={grillaFormulario}>
          {id ? (
            <MyTextField label="Empresa" name="empresa_nombre" control={control} disabled />
          ) : (
            <MyMultiSelectField
              label="Empresas"
              name="empresas"
              control={control}
              options={empresas}
              flotante
            />
          )}
          <MyTextField label="Límite de crédito" name="limite_credito" control={control} type="number" />
          <MyTextField label="Días de crédito" name="dias_credito" control={control} type="number" />
          <MyTextField label="Observaciones" name="observaciones" control={control} />
        </Box>
      </Seccion>
    </FormLayout>
  )
}

export default ClienteForm
