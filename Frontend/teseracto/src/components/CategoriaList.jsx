import CategoryIcon from '@mui/icons-material/CategoryOutlined'
import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'nombre', header: 'Nombre', size: 220 },
  { accessorKey: 'padre_nombre', header: 'Categoría padre', size: 200 },
  { accessorKey: 'empresas_nombres', header: 'Empresas', size: 320 },
]

const CategoriaList = () => (
  <CrudTable
    titulo="Categorías"
    subtitulo="Gestiona las categorías y las empresas que las usan."
    textoNuevo="Nueva categoría"
    icono={CategoryIcon}
    endpoint="categorias"
    rutaBase="/categorias"
    idKey="codigo"
    columns={columns}
    campoEstado="estado"
    valorActivo="A"
    valorInactivo="I"
  />
)

export default CategoriaList
