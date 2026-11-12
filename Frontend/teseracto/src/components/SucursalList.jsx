import { useParams } from 'react-router-dom'
import StoreIcon from '@mui/icons-material/StorefrontOutlined'
import CrudTable from './CrudTable'


const columns = [
  { accessorKey: 'nombre', header: 'Nombre', size: 200 },
  { accessorKey: 'telefono', header: 'Teléfono' },
  { accessorKey: 'calle_principal', header: 'Calle principal' },
  { accessorKey: 'localidad_nombre', header: 'Localidad' },
]

const SucursalList = () => {
  const { empresaId } = useParams()
  return (
    <CrudTable
      titulo="Sucursales"
      subtitulo="Gestiona las sucursales de la empresa."
      textoNuevo="Nueva sucursal"
      icono={StoreIcon}
      endpoint="sucursales"
      rutaBase={`/empresas/${empresaId}/sucursales`}
      params={{ empresa: empresaId }}
      idKey="codigo"
      columns={columns}
      campoEstado="estado"
      valorActivo="A"
      valorInactivo="I"
      rutaVolver="/empresas"
    />
  )
}

export default SucursalList
