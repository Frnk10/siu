import BadgeIcon from '@mui/icons-material/BadgeOutlined'
import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'identificacion', header: 'Identificación', size: 140 },
  { id: 'nombre', header: 'Nombre', size: 220, accessorFn: (r) => `${r.first_name} ${r.last_name}` },
  { accessorKey: 'username', header: 'Usuario', size: 140 },
  { accessorKey: 'empresa_nombre', header: 'Empresa', size: 200 },
  { accessorKey: 'sucursal_nombre', header: 'Sucursal', size: 160 },
  { accessorKey: 'fecha_ingreso', header: 'Fecha de ingreso', size: 140 },
]

const EmpleadoList = () => (
  <CrudTable
    titulo="Empleados"
    subtitulo="Gestiona los empleados de la empresa."
    textoNuevo="Nuevo empleado"
    icono={BadgeIcon}
    endpoint="empleados"
    rutaBase="/empleados"
    columns={columns}
    campoEstado="estado"
    valorActivo="A"
    valorInactivo="I"
  />
)

export default EmpleadoList
