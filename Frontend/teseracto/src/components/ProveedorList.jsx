import LocalShippingIcon from '@mui/icons-material/LocalShippingOutlined'
import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'identificacion', header: 'Identificación', size: 140 },
  { accessorKey: 'nombre', header: 'Nombre', size: 220 },
  { accessorKey: 'telefono1', header: 'Teléfono', size: 120 },
  { accessorKey: 'email', header: 'Correo', size: 200 },
  { accessorKey: 'banco', header: 'Banco', size: 150 },
  { accessorKey: 'empresa_nombre', header: 'Empresa', size: 200 },
]

const ProveedorList = () => (
  <CrudTable
    titulo="Proveedores"
    subtitulo="Gestiona los proveedores de tus empresas."
    textoNuevo="Nuevo proveedor"
    icono={LocalShippingIcon}
    endpoint="proveedores"
    rutaBase="/proveedores"
    columns={columns}
    campoEstado="estado"
    valorActivo="A"
    valorInactivo="I"
  />
)

export default ProveedorList
