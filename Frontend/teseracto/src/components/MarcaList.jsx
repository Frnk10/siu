import LocalOfferIcon from '@mui/icons-material/LocalOfferOutlined'
import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'nombre', header: 'Nombre', size: 220 },
  { accessorKey: 'empresas_nombres', header: 'Empresas', size: 320 },
]

const MarcaList = () => (
  <CrudTable
    titulo="Marcas"
    subtitulo="Gestiona las marcas y las empresas que las usan."
    textoNuevo="Nueva marca"
    icono={LocalOfferIcon}
    endpoint="marcas"
    rutaBase="/marcas"
    idKey="codigo"
    columns={columns}
    campoEstado="estado"
    valorActivo="A"
    valorInactivo="I"
  />
)

export default MarcaList
