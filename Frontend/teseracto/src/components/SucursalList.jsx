import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'empresa_nombre', header: 'Empresa', size: 220 },
  { accessorKey: 'nombre', header: 'Sucursal', size: 200 },
  { accessorKey: 'localidad_nombre', header: 'Localidad' },
  { accessorKey: 'calle_principal', header: 'Calle principal' },
  { accessorKey: 'calle_secundaria', header: 'Calle secundaria' },
]

const SucursalList = () => (
  <CrudTable titulo="Sucursales" endpoint="sucursales" rutaBase="/sucursales" idKey="codigo" columns={columns} />
)

export default SucursalList
