import StraightenIcon from '@mui/icons-material/StraightenOutlined'
import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'abreviatura', header: 'Abreviatura', size: 140 },
  { accessorKey: 'nombre', header: 'Nombre', size: 220 },
  { accessorKey: 'empresas_nombres', header: 'Empresas', size: 320 },
]

const UnidadMedidaList = () => (
  <CrudTable
    titulo="Unidades de medida"
    subtitulo="Gestiona las unidades de medida y las empresas que las usan."
    textoNuevo="Nueva unidad"
    icono={StraightenIcon}
    endpoint="unidades_medida"
    rutaBase="/unidades_medida"
    idKey="codigo"
    columns={columns}
    campoEstado="estado"
    valorActivo="A"
    valorInactivo="I"
  />
)

export default UnidadMedidaList
