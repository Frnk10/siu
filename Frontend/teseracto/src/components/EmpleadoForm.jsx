import { useEffect, useMemo, useState } from 'react'
import { Box, CircularProgress } from '@mui/material'
import BadgeIcon from '@mui/icons-material/BadgeOutlined'
import WorkIcon from '@mui/icons-material/WorkOutline'
import LockIcon from '@mui/icons-material/LockOutlined'
import AccountBalanceIcon from '@mui/icons-material/AccountBalanceOutlined'
import ContactPhoneIcon from '@mui/icons-material/ContactPhoneOutlined'
import { useForm, useWatch } from 'react-hook-form'
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

const crearSchema = (esEdicion) =>
  yup.object({
    ...personaSchema,
    username: yup
      .string()
      .trim()
      .max(150, 'El usuario no puede superar los 150 caracteres.')
      .matches(/^[\w.@+-]*$/, 'El usuario solo puede tener letras, números y @ . + - _'),
    password: yup
      .string()
      .test('largo', 'La contraseña debe tener al menos 8 caracteres.', (v) => !v || v.length >= 8)
      .test('requerida', 'La contraseña es obligatoria.', (v) => esEdicion || !!v),
    empresa: yup.string().required('Selecciona la empresa.'),
    sucursal: yup.string().nullable(),
    fecha_ingreso: yup.string().required('La fecha de ingreso es obligatoria.'),
    fecha_nacimiento: yup.string().nullable(),
    salario: yup
      .number()
      .nullable()
      .transform((v, o) => (o === '' ? null : v))
      .typeError('Ingresa un número válido.')
      .min(0, 'El salario no puede ser negativo.')
      .max(9999999999.99, 'El salario es demasiado alto.'),
    banco: yup.string().trim().max(100).matches(TEXTO_RE, MSG_ESPECIALES('El banco')),
    tipo_cuenta: yup.string().nullable(),
    numero_cuenta: yup.string().trim().max(30).matches(/^\d*$/, 'El número de cuenta solo puede tener dígitos.'),
    contacto_emergencia: yup.string().trim().max(150).matches(TEXTO_RE, MSG_ESPECIALES('El contacto de emergencia')),
    descripcion_emergencia: yup.string().trim().max(250).matches(TEXTO_RE, MSG_ESPECIALES('La descripción')),
  })

const valoresIniciales = {
  ...personaIniciales,
  username: '',
  password: '',
  empresa: '',
  sucursal: '',
  fecha_ingreso: '',
  fecha_nacimiento: '',
  salario: '',
  banco: '',
  tipo_cuenta: '',
  numero_cuenta: '',
  contacto_emergencia: '',
  descripcion_emergencia: '',
}

const EmpleadoForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const volver = '/empleados'
  const empresas = useMisEmpresas()
  const schema = useMemo(() => crearSchema(!!id), [id])

  const [sucursales, setSucursales] = useState([])
  const [cargando, setCargando] = useState(!!id)
  const [errorGeneral, setErrorGeneral] = useState('')

  const {
    handleSubmit, control, reset, setError, setValue,
    formState: { isSubmitting },
  } = useForm({ defaultValues: valoresIniciales, resolver: yupResolver(schema) })

  const empresa = useWatch({ control, name: 'empresa' })

  useEffect(() => {
    if (!id) return
    let activo = true
    AxiosInstance.get(`empleados/${id}/`)
      .then((r) => {
        if (!activo) return
        const d = r.data
        reset({
          ...personaDesdeApi(d),
          username: d.username ?? '',
          password: '',
          empresa: d.empresa ?? '',
          sucursal: d.sucursal ?? '',
          fecha_ingreso: d.fecha_ingreso ?? '',
          fecha_nacimiento: d.fecha_nacimiento ?? '',
          salario: d.salario ?? '',
          banco: d.banco ?? '',
          tipo_cuenta: d.tipo_cuenta ?? '',
          numero_cuenta: d.numero_cuenta ?? '',
          contacto_emergencia: d.contacto_emergencia ?? '',
          descripcion_emergencia: d.descripcion_emergencia ?? '',
        })
      })
      .catch(() => activo && setErrorGeneral('No se pudo cargar la información del empleado.'))
      .finally(() => activo && setCargando(false))
    return () => { activo = false }
  }, [id, reset])

  useEffect(() => {
    if (!id && empresas.length === 1) setValue('empresa', empresas[0].id)
  }, [id, empresas, setValue])

  // Sucursales de la empresa elegida
  useEffect(() => {
    if (!empresa) { setSucursales([]); return }
    let activo = true
    AxiosInstance.get('sucursales/', { params: { empresa } })
      .then((r) =>
        activo &&
        setSucursales(r.data.filter((s) => s.estado === 'A').map((s) => ({ id: s.codigo, name: s.nombre })))
      )
      .catch(() => activo && setSucursales([]))
    return () => { activo = false }
  }, [empresa])

  const enviar = (data) => {
    const payload = {
      ...personaAPayload(data),
      empresa: data.empresa,
      sucursal: data.sucursal || null,
      fecha_ingreso: data.fecha_ingreso,
      fecha_nacimiento: data.fecha_nacimiento || null,
      salario: data.salario ?? null,
      banco: data.banco ?? '',
      tipo_cuenta: data.tipo_cuenta ?? '',
      numero_cuenta: data.numero_cuenta ?? '',
      contacto_emergencia: data.contacto_emergencia ?? '',
      descripcion_emergencia: data.descripcion_emergencia ?? '',
    }
    if (data.username) payload.username = data.username
    if (data.password) payload.password = data.password

    setErrorGeneral('')
    const peticion = id
      ? AxiosInstance.patch(`empleados/${id}/`, payload)
      : AxiosInstance.post('empleados/', payload)

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
      titulo={id ? 'Editar empleado' : 'Nuevo empleado'}
      subtitulo={id ? 'Modifica los datos del empleado.' : 'Completa los datos para registrar un nuevo empleado.'}
      icono={BadgeIcon}
      onSubmit={handleSubmit(enviar)}
      errorGeneral={errorGeneral}
      enviando={isSubmitting}
      onCancelar={() => navigate(volver)}
    >
      <PersonaCampos control={control} setValue={setValue} edicion={!!id} mostrarTipo={false} />

      <Seccion titulo="Acceso al sistema" icono={LockIcon}>
        <Box sx={grillaFormulario}>
          <MyTextField label="Usuario (opcional, por defecto la identificación)" name="username" control={control} />
          <MyTextField
            label={id ? 'Nueva contraseña (opcional)' : 'Contraseña'}
            name="password"
            control={control}
            type="password"
            required={!id}
          />
        </Box>
      </Seccion>

      <Seccion titulo="Datos laborales" icono={WorkIcon}>
        <Box sx={grillaFormulario}>
          <MySelectField
            label="Empresa"
            name="empresa"
            control={control}
            options={empresas}
            flotante
            onCambio={() => setValue('sucursal', '')}
          />
          <MySelectField
            label="Sucursal"
            name="sucursal"
            control={control}
            options={sucursales}
            flotante
            disabled={!empresa}
          />
          <MyTextField label="Fecha de ingreso" name="fecha_ingreso" control={control} type="date" required />
          <MyTextField label="Fecha de nacimiento" name="fecha_nacimiento" control={control} type="date" />
          <MyTextField label="Salario" name="salario" control={control} type="number" />
        </Box>
      </Seccion>

      <Seccion titulo="Datos bancarios" icono={AccountBalanceIcon}>
        <Box sx={grillaFormulario}>
          <MyTextField label="Banco" name="banco" control={control} />
          <MySelectField label="Tipo de cuenta" name="tipo_cuenta" control={control} options={TIPOS_CUENTA} flotante />
          <MyTextField label="Número de cuenta" name="numero_cuenta" control={control} />
        </Box>
      </Seccion>

      <Seccion titulo="Contacto de emergencia" icono={ContactPhoneIcon}>
        <Box sx={grillaFormulario}>
          <MyTextField label="Contacto" name="contacto_emergencia" control={control} />
          <MyTextField label="Descripción" name="descripcion_emergencia" control={control} />
        </Box>
      </Seccion>
    </FormLayout>
  )
}

export default EmpleadoForm
