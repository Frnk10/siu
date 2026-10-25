import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'codigo_auxiliar', header: 'Código auxiliar', size: 180 },
  { accessorKey: 'nombre', header: 'Nombre', size: 200 },
  { accessorKey: 'grupo', header: 'Grupo' },
  { accessorKey: 'descripcion', header: 'Descripción', size: 260 },
]

const ConfiguracionList = () => (
  <CrudTable titulo="Configuraciones" endpoint="configuraciones" rutaBase="/configuraciones" idKey="codigo" columns={columns} />
)

export default ConfiguracionList
