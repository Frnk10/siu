import Dayjs from 'dayjs'
import { Avatar } from '@mui/material'
import BusinessIcon from '@mui/icons-material/Business'
import { IconButton, Tooltip } from '@mui/material'
import StoreIcon from '@mui/icons-material/StorefrontOutlined'
import SettingsIcon from '@mui/icons-material/SettingsOutlined'
import { Link } from 'react-router-dom'
import CrudTable, { botonCuadro } from './CrudTable'

const accionesExtra = (fila) => (
    <>
    <Tooltip title="Sucursales">
      <IconButton
        sx={botonCuadro('success')}
        component={Link}
        to={`/empresas/${fila.codigo}/sucursales`}
      >
        <StoreIcon sx={{ fontSize: 18 }} />
      </IconButton>
    </Tooltip>

    <Tooltip title="Configuración">
      <IconButton
        sx={botonCuadro('warning')}
        component={Link}
        to={`/empresas/${fila.codigo}/configuracion`}
      >
        <SettingsIcon sx={{ fontSize: 18 }} />
      </IconButton>
    </Tooltip>
  </>
)

const columns = [
  {
    accessorKey: 'logotipo',
    header: 'Logotipo',
    size: 100,
    enableSorting: false,
    enableColumnFilter: false,
    Cell: ({ cell }) => {
      const url = cell.getValue()
      return (
        <Avatar variant="rounded" src={url || undefined} alt="Logotipo" slotProps={{ img: { style: { objectFit: 'contain' } } }} sx={{ width: 48, height: 48, bgcolor: '#fff', border: '1px solid #e0e0e0' }}>
          <BusinessIcon />
        </Avatar>
      )
    },
  },
  { accessorKey: 'razon_social', header: 'Razón social', size: 220 },
  { accessorKey: 'representante_nombre', header: 'Representante' },
  { accessorKey: 'telefono', header: 'Teléfono' },
  { accessorKey: 'localidad_nombre', header: 'Localidad' },
  {
    id: 'fecha_constitucion',
    header: 'Constitución',
    accessorFn: (r) => (r.fecha_constitucion ? Dayjs(r.fecha_constitucion).format('DD-MM-YYYY') : ''),
  },
  { id: 'contabilidad', header: 'Oblig. contabilidad', accessorFn: (r) => (r.obligado_contabilidad ? 'Sí' : 'No') },
  { id: 'factura', header: 'Fact. electrónica', accessorFn: (r) => (r.facturacion_electronica ? 'Sí' : 'No') },
]

const EmpresaList = () => (
  <CrudTable
    titulo="Empresas"
    subtitulo="Gestiona los registros de empresas."
    textoNuevo="Nueva empresa"
    icono={BusinessIcon}
    endpoint="empresas"
    rutaBase="/empresas"
    idKey="codigo"
    columns={columns}
    campoEstado="estado"
    valorActivo="A"
    valorInactivo="I"
    accionesExtra={accionesExtra}
  />
)

export default EmpresaList
