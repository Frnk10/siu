import { useCallback, useEffect, useMemo, useState } from 'react'
import { MaterialReactTable } from 'material-react-table'
import { MRT_Localization_ES } from 'material-react-table/locales/es'
import { Alert, Box, Button, IconButton, Pagination, Tooltip, Typography } from '@mui/material'
import { alpha, darken, lighten } from '@mui/material/styles'
import AddIcon from '@mui/icons-material/Add'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/DeleteOutlined'
import CheckIcon from '@mui/icons-material/CheckCircleOutlined'
import Inventory2Icon from '@mui/icons-material/Inventory2'
import { Link } from 'react-router-dom'
import AxiosInstance from './AxiosInstance'
import Swal from 'sweetalert2'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'

export const botonCuadro = (tono) => ({
  width: 32,
  height: 32,
  borderRadius: '8px',
  color: `${tono}.main`,
  bgcolor: (t) => lighten(t.palette[tono].main, 0.88),
  '&:hover': { bgcolor: (t) => lighten(t.palette[tono].main, 0.78) },
})

const navy = (t) => darken(t.palette.primary.main, 0.45)

// Encabezado: fondo primary, letras e iconos blancos
const estiloEncabezado = {
  bgcolor: 'primary.main',
  color: '#fff',
  fontWeight: 700,
  fontSize: 13,
  py: 1,
  '& .MuiTableSortLabel-root, & .MuiTableSortLabel-icon': { color: '#fff !important' },
  '& .MuiCheckbox-root, & .MuiCheckbox-root.Mui-checked, & .MuiCheckbox-root.MuiCheckbox-indeterminate': {
    color: '#fff',
  },
  '& .Mui-TableHeadCell-Content-Actions .MuiIconButton-root': { color: '#fff' },
}

// Props: titulo, subtitulo, textoNuevo, icono, endpoint, rutaBase, idKey, columns,
// campoEstado, valorActivo, valorInactivo.
// `columns` debe definirse fuera del componente para que sea estable.
const CrudTable = ({
  titulo,
  subtitulo,
  textoNuevo = 'Nuevo',
  icono: IconoTitulo = Inventory2Icon,
  endpoint,
  rutaBase,
  idKey = 'id',
  columns,
  campoEstado = 'estado',
  valorActivo = 1,
  valorInactivo = 0,
  accionesExtra,
  params,
  rutaVolver,
}) => {
  const [data, setData] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  const paramsKey = JSON.stringify(params ?? {})

  const cargar = useCallback(() => {
    setCargando(true)
    AxiosInstance.get(`${endpoint}/`, { params: JSON.parse(paramsKey) })
      .then((res) => setData(res.data))
      .catch(() => setError('No se pudo cargar la información.'))
      .finally(() => setCargando(false))
  }, [endpoint, paramsKey])

  useEffect(() => {
    cargar()
  }, [cargar])

  const tieneEstado = useCallback(
    (fila) => !!campoEstado && fila[campoEstado] !== undefined && fila[campoEstado] !== null,
    [campoEstado]
  )
  const esActivo = useCallback(
    (fila) => {
      const v = fila[campoEstado]
      return typeof v === 'boolean' ? v : String(v) === String(valorActivo)
    },
    [campoEstado, valorActivo]
  )

  const mensajeError = (err) => {
    const data = err.response?.data
    if (data?.detail) return Array.isArray(data.detail) ? data.detail.join(' ') : data.detail
    if (data && typeof data === 'object') return Object.values(data).flat().join(' ')
    return 'No se pudo cambiar el estado del registro.'
  }

  const cambiarEstado = async (fila) => {
    const activo = esActivo(fila)

    const { isConfirmed } = await Swal.fire({
      title: activo ? '¿Desactivar registro?' : '¿Activar registro?',
      text: activo
        ? 'El registro quedará inactivo, pero no se eliminará.'
        : 'El registro volverá a estar activo.',
      icon: activo ? 'warning' : 'question',
      showCancelButton: true,
      confirmButtonText: activo ? 'Sí, desactivar' : 'Sí, activar',
      cancelButtonText: 'Cancelar',
      confirmButtonColor: activo ? '#d32f2f' : '#2e7d32',
      reverseButtons: true,
      focusCancel: activo,
    })
    if (!isConfirmed) return

    const url = `${endpoint}/${fila[idKey]}/`

    try {
      // Desactivar -> DELETE (borrado lógico, ejecuta validar_baja)
      // Activar    -> PATCH con estado "A"
      if (activo) await AxiosInstance.delete(url)
      else await AxiosInstance.patch(url, { [campoEstado]: valorActivo })

      cargar()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: activo ? 'Registro desactivado' : 'Registro activado',
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
      })
    } catch (err) {
      Swal.fire({
        icon: 'error',
        title: 'No se pudo completar la acción',
        text: mensajeError(err),
        confirmButtonText: 'Entendido',
      })
    }
  }

  // Columna Estado con píldora y filtro desplegable (Activo / Inactivo)
  const columnasFinales = useMemo(() => {
    if (!campoEstado) return columns
    return [
      ...columns,
      {
        id: '__estado',
        header: 'Estado',
        size: 130,
        filterVariant: 'select',
        filterSelectOptions: ['Activo', 'Inactivo'],
        accessorFn: (r) => (tieneEstado(r) ? (esActivo(r) ? 'Activo' : 'Inactivo') : ''),
        Cell: ({ cell }) => {
          const valor = cell.getValue()
          if (!valor) return null
          const tono = valor === 'Activo' ? 'success' : 'error'
          return (
            <Box
              sx={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 0.6,
                px: 1.25,
                py: 0.3,
                borderRadius: '999px',
                fontSize: 12,
                fontWeight: 600,
                color: `${tono}.dark`,
                bgcolor: (t) => lighten(t.palette[tono].main, 0.86),
              }}
            >
              <Box sx={{ width: 7, height: 7, borderRadius: '50%', bgcolor: 'currentColor' }} />
              {valor}
            </Box>
          )
        },
      },
    ]
  }, [columns, campoEstado, tieneEstado, esActivo])

  return (
    <Box
      sx={{
        bgcolor: '#fff',
        borderRadius: 3,
        p: { xs: 1.5, sm: 2.5 },
        boxShadow: (t) => `0 2px 12px ${alpha(t.palette.primary.main, 0.08)}`,
      }}
    >
      {/* Título, subtítulo y botón: dentro de la tarjeta */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: 2,
          mb: 2,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          {rutaVolver && (
            <Tooltip title="Volver">
              <IconButton component={Link} to={rutaVolver} sx={botonCuadro('primary')}>
                <ArrowBackIcon sx={{ fontSize: 18 }} />
              </IconButton>
            </Tooltip>
          )}
          <Box
            sx={{
              width: 46,
              height: 46,
              borderRadius: '50%',
              display: 'grid',
              placeItems: 'center',
              color: 'primary.main',
              bgcolor: (t) => lighten(t.palette.primary.main, 0.88),
            }}
          >
            <IconoTitulo sx={{ fontSize: 24 }} />
          </Box>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 800, color: navy, lineHeight: 1.2 }}>
              {titulo}
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              {subtitulo || `Gestiona los registros de ${titulo.toLowerCase()}.`}
            </Typography>
          </Box>
        </Box>

        <Button
          component={Link}
          to={`${rutaBase}/crear`}
          variant="contained"
          startIcon={<AddIcon />}
          sx={{ borderRadius: '8px', px: 2, py: 0.8, fontSize: 14, fontWeight: 700, textTransform: 'none', boxShadow: 'none' }}
        >
          {textoNuevo}
        </Button>
      </Box>

      {error && (
        <Alert severity="error" onClose={() => setError('')} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <MaterialReactTable
        columns={columnasFinales}
        data={data}
        localization={MRT_Localization_ES}
        state={{ isLoading: cargando }}
        // Herramientas nativas: buscador global, filtros por columna,
        // mostrar/ocultar columnas, densidad y pantalla completa
        enableGlobalFilter
        enableColumnFilters
        enableColumnActions
        enableHiding
        enableDensityToggle
        enableFullScreenToggle
        globalFilterFn="contains"
        enableRowSelection
        enableColumnPinning
        initialState={{
          density: 'compact',
          pagination: { pageIndex: 0, pageSize: 10 },
          columnPinning: { right: ['mrt-row-actions'] },
          showGlobalFilter: true,
        }}
        // Acciones fijas a la derecha
        enableRowActions
        positionActionsColumn="last"
        displayColumnDefOptions={{
          'mrt-row-select': {
            size: 50,
            muiTableHeadCellProps: { sx: estiloEncabezado },
          },
          'mrt-row-actions': {
            header: 'Acciones',
            size: 100,
            muiTableHeadCellProps: { align: 'center', sx: estiloEncabezado },
            muiTableBodyCellProps: { align: 'center', sx: { bgcolor: '#fff' } },
          },
        }}
        renderRowActions={({ row }) => {
          const fila = row.original
          const conEstado = tieneEstado(fila)
          const activo = conEstado && esActivo(fila)
          return (
            <Box sx={{ display: 'flex', flexWrap: 'nowrap', justifyContent: 'center', gap: 0.75 }}>
              <Tooltip title="Editar">
                <IconButton sx={botonCuadro('primary')} component={Link} to={`${rutaBase}/editar/${fila[idKey]}`}>
                  <EditIcon sx={{ fontSize: 18 }} />
                </IconButton>
              </Tooltip>

              {conEstado && (
                <Tooltip title={activo ? 'Desactivar' : 'Activar'}>
                  <IconButton sx={botonCuadro(activo ? 'error' : 'success')} onClick={() => cambiarEstado(fila)}>
                    {activo ? <DeleteIcon sx={{ fontSize: 18 }} /> : <CheckIcon sx={{ fontSize: 18 }} />}
                  </IconButton>
                </Tooltip>
              )}
              {accionesExtra?.(fila)}
            </Box>
          )
        }}
        // Diseño
        muiTablePaperProps={({ table }) => ({
          elevation: 0,
          sx: {
            bgcolor: '#fff',
            boxShadow: 'none',
            border: (t) => `1px solid ${lighten(t.palette.primary.main, 0.85)}`,
            borderRadius: table.getState().isFullScreen ? 0 : 2,
            overflow: 'hidden',
          },
        })}
        muiTopToolbarProps={{ sx: { bgcolor: '#fff', py: 0.5 } }}
        muiTableContainerProps={{ sx: { bgcolor: '#fff' } }}
        muiTableHeadCellProps={{ sx: estiloEncabezado }}
        muiTableBodyCellProps={{ sx: { bgcolor: '#fff', fontSize: 13 } }}
        // Pie: "Mostrando 1 - 8 de 8 registros" y paginación
        renderBottomToolbar={({ table }) => {
          const { pageIndex, pageSize } = table.getState().pagination
          const total = table.getFilteredRowModel().rows.length
          const desde = total === 0 ? 0 : pageIndex * pageSize + 1
          const hasta = Math.min((pageIndex + 1) * pageSize, total)
          return (
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: 2,
                p: 1.5,
              }}
            >
              <Typography variant="body2" sx={{ color: 'text.secondary', fontSize: 13 }}>
                {total === 0 ? 'Sin registros' : `Mostrando ${desde} - ${hasta} de ${total} registros`}
              </Typography>
              <Pagination
                count={table.getPageCount()}
                page={pageIndex + 1}
                onChange={(_, pagina) => table.setPageIndex(pagina - 1)}
                variant="outlined"
                color="primary"
                shape="rounded"
                sx={{
                  '& .MuiPaginationItem-root': {
                    borderRadius: '8px',
                    color: 'primary.main',
                    borderColor: (t) => lighten(t.palette.primary.main, 0.8),
                  },
                  '& .MuiPaginationItem-root.Mui-selected': {
                    bgcolor: 'primary.main',
                    color: '#fff',
                    borderColor: 'primary.main',
                    fontWeight: 700,
                    '&:hover': { bgcolor: 'primary.dark' },
                  },
                }}
              />
            </Box>
          )
        }}
      />
    </Box>
  )
}

export default CrudTable
