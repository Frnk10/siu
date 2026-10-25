export const aplicarErroresServidor = (error, setError, setErrorGeneral) => {
  const datos = error.response?.data
  if (error.response?.status === 400 && datos && typeof datos === 'object') {
    const generales = []
    Object.entries(datos).forEach(([campo, msg]) => {
      const texto = Array.isArray(msg) ? msg.join(' ') : String(msg)
      if (campo === 'non_field_errors' || campo === 'detail') generales.push(texto)
      else setError(campo, { type: 'server', message: texto })
    })
    setErrorGeneral(generales.join(' '))
  } else {
    setErrorGeneral('Ocurrió un error inesperado. Intenta nuevamente.')
  }
}