import HomeIcon from '@mui/icons-material/Home'
import BorderColorIcon from '@mui/icons-material/BorderColor'
import BusinessIcon from '@mui/icons-material/Business'
import StoreIcon from '@mui/icons-material/Store'
import SettingsIcon from '@mui/icons-material/Settings'
import PeopleIcon from '@mui/icons-material/People'
import FolderIcon from '@mui/icons-material/Folder'

// El nombre guardado en Menu.icono debe coincidir con una clave de este mapa.
// Para usar otro icono, impórtalo y agrégalo aquí.
const ICONOS = {
  Home: HomeIcon,
  BorderColor: BorderColorIcon,
  Store: StoreIcon,
  LocationCityIcon: BusinessIcon,
  Settings: SettingsIcon,
  People: PeopleIcon,
  Folder: FolderIcon,
}

export const obtenerIcono = (nombre) => ICONOS[nombre] || FolderIcon