import { useParams } from 'react-router-dom'
import SettingsIcon from '@mui/icons-material/SettingsOutlined'
import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'configuracion_nombre', header: 'Configuración', size: 220 },
  { accessorKey: 'valor', header: 'Valor', size: 300 },
]

const EmpresaConfiguracionList = () => {
  const { empresaId } = useParams()
  return (
    <CrudTable
      titulo="Configuración de la empresa"
      subtitulo="Gestiona los valores de configuración asignados a esta empresa."
      textoNuevo="Agregar configuración"
      icono={SettingsIcon}
      endpoint="empresa_configuraciones"
      rutaBase={`/empresas/${empresaId}/configuracion`}
      params={{ empresa: empresaId }}
      rutaVolver="/empresas"
      idKey="id"
      columns={columns}
      campoEstado="estado"
      valorActivo="A"
      valorInactivo="I"
    />
  )
}

export default EmpresaConfiguracionList
