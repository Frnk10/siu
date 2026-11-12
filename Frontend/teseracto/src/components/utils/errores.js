export const aplicarErroresServidor = (err, setError, setErrorGeneral) => {
  const data = err.response?.data
  console.log('Errores del servidor:', JSON.stringify(data))

  if (!data || typeof data !== 'object') {
    setErrorGeneral('No se pudo guardar. Intenta de nuevo.')
    return
  }

  Object.entries(data).forEach(([campo, msgs]) => {
    const mensaje = Array.isArray(msgs) ? msgs.join(' ') : String(msgs)
    if (campo === 'detail' || campo === 'non_field_errors') {
      setErrorGeneral(mensaje)
    } else {
      setError(campo, { type: 'server', message: mensaje }, { shouldFocus: false })
    }
  })
}