import { useCallback, useEffect, useState } from 'react'
import { MaterialReactTable } from 'material-react-table'
import { Alert, Box, Button, IconButton, Typography } from '@mui/material'
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material'
import { Link } from 'react-router-dom'
import AxiosInstance from './AxiosInstance';

// Tabla genérica: lista, y permite crear / editar / eliminar.
// `columns` debe definirse fuera del componente para que sea estable.
const CrudTable = ({ titulo, endpoint, rutaBase, idKey = 'id', columns }) => {
  const [data, setData] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  const cargar = useCallback(() => {
    setCargando(true)
    AxiosInstance.get(`${endpoint}/`)
      .then((res) => setData(res.data))
      .catch(() => setError('No se pudo cargar la información.'))
      .finally(() => setCargando(false))
  }, [endpoint])

  useEffect(() => {
    cargar()
  }, [cargar])

  const eliminar = (id) => {
    if (!window.confirm('¿Seguro que deseas eliminar este registro?')) return
    AxiosInstance.delete(`${endpoint}/${id}/`)
      .then(cargar)
      .catch((err) => {
        const d = err.response?.data?.detail
        setError(Array.isArray(d) ? d.join(' ') : d || 'No se pudo eliminar el registro.')
      })
  }

  return (
    <div>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: '#00003f',
          marginBottom: '10px',
          padding: '4px 20px',
        }}
      >
        <Typography sx={{ color: '#fff' }}>{titulo}</Typography>
        <Button component={Link} to={`${rutaBase}/crear`} variant="contained" size="small" startIcon={<AddIcon />}>
          Nuevo
        </Button>
      </Box>

      {error && (
        <Alert severity="error" onClose={() => setError('')} sx={{ marginBottom: '10px' }}>
          {error}
        </Alert>
      )}

      <MaterialReactTable
        columns={columns}
        data={data}
        state={{ isLoading: cargando }}
        enableRowActions
        renderRowActions={({ row }) => (
          <Box sx={{ display: 'flex', flexWrap: 'nowrap', gap: '8px' }}>
            <IconButton color="secondary" component={Link} to={`${rutaBase}/editar/${row.original[idKey]}`}>
              <EditIcon />
            </IconButton>
            <IconButton color="error" onClick={() => eliminar(row.original[idKey])}>
              <DeleteIcon />
            </IconButton>
          </Box>
        )}
      />
    </div>
  )
}

export default CrudTable
