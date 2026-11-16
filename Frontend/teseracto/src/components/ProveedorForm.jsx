import { useEffect, useState } from 'react'
import { Box, CircularProgress } from '@mui/material'
import LocalShippingIcon from '@mui/icons-material/LocalShippingOutlined'
import AccountBalanceIcon from '@mui/icons-material/AccountBalanceOutlined'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import { useNavigate, useParams } from 'react-router-dom'

import AxiosInstance from './AxiosInstance'
import FormLayout, { Seccion } from './FormLayout'
import MyTextField from './forms/MyTextField'
import MySelectField from './forms/MySelectField'
import { aplicarErroresServidor } from './utils/errores'
import {
  PersonaCampos, personaSchema, personaIniciales, personaDesdeApi, personaAPayload,
  useMisEmpresas, grillaFormulario, TEXTO_RE, MSG_ESPECIALES, TIPOS_CUENTA,
} from './PersonaCampos'

const schema = yup.object({
  ...personaSchema,
  empresa: yup.string().nullable(),
  link_catalogo: yup.string().trim().url('Ingresa un enlace válido (https://...).'),
  banco: yup.string().trim().max(100, 'El banco no puede superar los 100 caracteres.').matches(TEXTO_RE, MSG_ESPECIALES('El banco')),
  tipo_cuenta: yup.string().nullable(),
  numero_cuenta: yup
    .string()
    .trim()
    .max(30, 'El número de cuenta no puede superar los 30 caracteres.')
    .matches(/^\d*$/, 'El número de cuenta solo puede tener dígitos.'),
  observaciones: yup.string().trim().matches(TEXTO_RE, MSG_ESPECIALES('Las observaciones')),
})

const valoresIniciales = {
  ...personaIniciales,
  empresa: '',
  link_catalogo: '',
  banco: '',
  tipo_cuenta: '',
  numero_cuenta: '',
  observaciones: '',
}

const ProveedorForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const volver = '/proveedores'
  const empresas = useMisEmpresas()

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
    AxiosInstance.get(`proveedores/${id}/`)
      .then((r) => {
        if (!activo) return
        const d = r.data
        setCompartido(!!d.datos_compartidos)
        reset({
          ...personaDesdeApi(d),
          empresa: d.empresa ?? '',
          link_catalogo: d.link_catalogo ?? '',
          banco: d.banco ?? '',
          tipo_cuenta: d.tipo_cuenta ?? '',
          numero_cuenta: d.numero_cuenta ?? '',
          observaciones: d.observaciones ?? '',
        })
      })
      .catch(() => activo && setErrorGeneral('No se pudo cargar la información del proveedor.'))
      .finally(() => activo && setCargando(false))
    return () => { activo = false }
  }, [id, reset])

  useEffect(() => {
    if (!id && empresas.length === 1) setValue('empresa', empresas[0].id)
  }, [id, empresas, setValue])

  const enviar = (data) => {
    const payload = {
      ...personaAPayload(data),
      link_catalogo: data.link_catalogo || null,
      banco: data.banco ?? '',
      tipo_cuenta: data.tipo_cuenta ?? '',
      numero_cuenta: data.numero_cuenta ?? '',
      observaciones: data.observaciones ?? '',
    }
    if (!id && data.empresa) payload.empresa = data.empresa

    setErrorGeneral('')
    const peticion = id
      ? AxiosInstance.patch(`proveedores/${id}/`, payload)
      : AxiosInstance.post('proveedores/', payload)

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
      titulo={id ? 'Editar proveedor' : 'Nuevo proveedor'}
      subtitulo={id ? 'Modifica los datos del proveedor.' : 'Si la identificación ya existe, se reutilizan sus datos.'}
      icono={LocalShippingIcon}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate(volver)}
    >
      <PersonaCampos control={control} setValue={setValue} edicion={!!id} bloqueado={compartido} />

      <Seccion titulo="Datos del proveedor" icono={AccountBalanceIcon}>
        <Box sx={grillaFormulario}>
          {!id && empresas.length > 1 && (
            <MySelectField label="Empresa" name="empresa" control={control} options={empresas} flotante />
          )}
          <MyTextField label="Enlace del catálogo" name="link_catalogo" control={control} disabled={compartido} />
          <MyTextField label="Banco" name="banco" control={control} disabled={compartido} />
          <MySelectField
            label="Tipo de cuenta"
            name="tipo_cuenta"
            control={control}
            options={TIPOS_CUENTA}
            flotante
            disabled={compartido}
          />
          <MyTextField label="Número de cuenta" name="numero_cuenta" control={control} disabled={compartido} />
          <MyTextField label="Observaciones" name="observaciones" control={control} disabled={compartido} />
        </Box>
      </Seccion>
    </FormLayout>
  )
}

export default ProveedorForm
