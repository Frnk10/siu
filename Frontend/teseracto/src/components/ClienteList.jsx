import PeopleIcon from '@mui/icons-material/PeopleAltOutlined'
import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'identificacion', header: 'Identificación', size: 140 },
  { accessorKey: 'nombre', header: 'Nombre', size: 220 },
  { accessorKey: 'telefono1', header: 'Teléfono', size: 120 },
  { accessorKey: 'email', header: 'Correo', size: 200 },
  { accessorKey: 'limite_credito', header: 'Límite de crédito', size: 150 },
  { accessorKey: 'dias_credito', header: 'Días de crédito', size: 130 },
  { accessorKey: 'empresa_nombre', header: 'Empresa', size: 200 },
]

const ClienteList = () => (
  <CrudTable
    titulo="Clientes"
    subtitulo="Gestiona los clientes de tus empresas."
    textoNuevo="Nuevo cliente"
    icono={PeopleIcon}
    endpoint="clientes"
    rutaBase="/clientes"
    columns={columns}
    campoEstado="estado"
    valorActivo="A"
    valorInactivo="I"
  />
)

export default ClienteList
