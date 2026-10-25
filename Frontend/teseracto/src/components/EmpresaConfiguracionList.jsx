import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'empresa_nombre', header: 'Empresa', size: 220 },
  { accessorKey: 'configuracion_grupo', header: 'Grupo' },
  { accessorKey: 'configuracion_nombre', header: 'Configuración', size: 200 },
  { accessorKey: 'valor', header: 'Valor', size: 240 },
]

const EmpresaConfiguracionList = () => (
  <CrudTable
    titulo="Configuración de empresa"
    endpoint="empresa_configuraciones"
    rutaBase="/empresa_configuraciones"
    idKey="id"
    columns={columns}
  />
)

export default EmpresaConfiguracionList
