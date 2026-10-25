import Dayjs from 'dayjs'
import CrudTable from './CrudTable'

const columns = [
  { accessorKey: 'razon_social', header: 'Razón social', size: 220 },
  { accessorKey: 'representante_nombre', header: 'Representante' },
  { accessorKey: 'telefono', header: 'Teléfono' },
  { accessorKey: 'localidad_nombre', header: 'Localidad' },
  {
    id: 'fecha_constitucion',
    header: 'Constitución',
    accessorFn: (r) => (r.fecha_constitucion ? Dayjs(r.fecha_constitucion).format('DD-MM-YYYY') : ''),
  },
  { id: 'contabilidad', header: 'Oblig. contabilidad', accessorFn: (r) => (r.obligado_contabilidad ? 'Sí' : 'No') },
  { id: 'factura', header: 'Fact. electrónica', accessorFn: (r) => (r.facturacion_electronica ? 'Sí' : 'No') },
]

const EmpresaList = () => (
  <CrudTable titulo="Empresas" endpoint="empresas" rutaBase="/empresas" idKey="codigo" columns={columns} />
)

export default EmpresaList
