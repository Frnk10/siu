import * as React from 'react';
import {
  Avatar,
  Badge,
  Box,
  Drawer,
  AppBar,
  CssBaseline,
  Toolbar,
  List,
  Typography,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Collapse,
  CircularProgress,
  InputBase,
  Menu,
  MenuItem,
} from '@mui/material';

import MenuIcon from '@mui/icons-material/Menu';
import LogoutIcon from '@mui/icons-material/Logout';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import SearchIcon from '@mui/icons-material/Search';
import NotificationsIcon from '@mui/icons-material/Notifications';
import PersonIcon from '@mui/icons-material/Person';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

import { alpha, darken, lighten, useTheme } from '@mui/material/styles';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import AxiosInstance from './AxiosInstance';
import { obtenerIcono } from './utils/iconos';

const ALTO_BARRA = 60;

// Logo: usa la imagen del backend (LOGO_URL). Si falla la carga, se muestra el cubo SVG.
const LogoTeseracto = ({ src, size = 36 }) => {
  const [fallo, setFallo] = React.useState(false);
  const theme = useTheme();

  if (src && !fallo) {
    return (
      <Box
        component="img"
        src={src}
        alt="Teseracto"
        onError={() => setFallo(true)}
        sx={{ height: size, width: 'auto', display: 'block' }}
      />
    );
  }

  const trazo = theme.palette.primary.main;
  return (
    <svg width={size} height={size} viewBox="0 0 48 48" aria-hidden="true">
      <path d="M24 3 43 13v22L24 45 5 35V13z" fill="#fff" />
      <path d="M24 24 43 13v22L24 45z" fill="#fff" fillOpacity="0.75" />
      <path d="M24 24 5 13 24 3l19 10z" fill="#fff" />
      <path d="M24 24v21" stroke={trazo} strokeWidth="3" />
      <path d="M24 24 9 16M24 24l15-8" stroke={trazo} strokeWidth="3" />
    </svg>
  );
};

// Ítems del menú: texto e iconos blancos sobre fondo azul (primary).
// Ítem de la ruta actual: píldora azul más oscura con texto en negrita.
const estiloItem = (nivel) => ({
  mx: nivel === 0 ? 1.25 : 2.5,
  my: 0.4,
  py: 0.8,
  pl: nivel === 0 ? 1.5 : 1.5,
  borderRadius: '10px',
  color: '#fff',
  '& .MuiListItemIcon-root': { minWidth: 36, color: 'inherit' },
  '& .MuiListItemIcon-root svg': { fontSize: 20 },
  '& .MuiListItemText-primary': { fontSize: 14, fontWeight: 500 },
  '&:hover': { backgroundColor: alpha('#fff', 0.12) },
  '&.Mui-selected': {
    backgroundColor: (t) => darken(t.palette.primary.main, 0.25),
    '& .MuiListItemText-primary': { fontWeight: 700 },
    '&:hover': { backgroundColor: (t) => darken(t.palette.primary.main, 0.25) },
  },
});

// ¿La ruta actual corresponde a este ítem? Ignora "/" inicial/final
// y también cuenta /clientes/5 para el ítem /clientes.
const limpiar = (u) => '/' + String(u ?? '').trim().replace(/^\/+|\/+$/g, '');
const coincideRuta = (url, path) => {
  if (!url) return false;
  const u = limpiar(url);
  const p = limpiar(path);
  return u === '/' ? p === '/' : p === u || p.startsWith(u + '/');
};

// Item recursivo: si tiene hijos se despliega, si no, es un enlace.
// Los hijos muestran un punto en lugar de icono.
const MenuNodo = ({ item, nivel, path, abiertos, alternar, cerrarDrawer }) => {
  const Icono = obtenerIcono(item.icono);
  const icono =
    nivel > 0 ? (
      <Box sx={{ width: 5, height: 5, borderRadius: '50%', bgcolor: 'currentColor', ml: 1 }} />
    ) : (
      <Icono />
    );

  if (item.hijos?.length > 0) {
    const abierto = !!abiertos[item.id];
    const hijoActivo = item.hijos.some((h) => coincideRuta(h.url, path));
    return (
      <>
        <ListItem disablePadding>
          <ListItemButton onClick={() => alternar(item.id)} selected={hijoActivo} sx={estiloItem(nivel)}>
            <ListItemIcon>{icono}</ListItemIcon>
            <ListItemText primary={item.nombre} />
            {abierto ? <ExpandLess fontSize="small" /> : <ExpandMore fontSize="small" />}
          </ListItemButton>
        </ListItem>

        <Collapse in={abierto} timeout="auto" unmountOnExit>
          <List disablePadding>
            {item.hijos.map((hijo) => (
              <MenuNodo
                key={hijo.id}
                item={hijo}
                nivel={nivel + 1}
                path={path}
                abiertos={abiertos}
                alternar={alternar}
                cerrarDrawer={cerrarDrawer}
              />
            ))}
          </List>
        </Collapse>
      </>
    );
  }

  if (!item.url) return null;

  return (
    <ListItem disablePadding>
      <ListItemButton
        component={Link}
        to={item.url}
        selected={coincideRuta(item.url, path)}
        onClick={cerrarDrawer}
        sx={estiloItem(nivel)}
      >
        <ListItemIcon>{icono}</ListItemIcon>
        <ListItemText primary={item.nombre} />
      </ListItemButton>
    </ListItem>
  );
};

const Navbar = (props) => {
  const { drawerWidth = 240, content, usuario, notificaciones = 0, version = '1.0.0' } = props;

  const location = useLocation();
  const navigate = useNavigate();
  const path = location.pathname;

  const [open, setOpen] = React.useState(false);
  const [menu, setMenu] = React.useState([]);
  const [cargandoMenu, setCargandoMenu] = React.useState(true);
  const [errorMenu, setErrorMenu] = React.useState(false);
  const [abiertos, setAbiertos] = React.useState({});
  const [logoUrl, setLogoUrl] = React.useState(null);
  const [anchorUsuario, setAnchorUsuario] = React.useState(null);

  // Nombre que se muestra arriba a la derecha
  const nombreUsuario = usuario || localStorage.getItem('Usuario') || 'Usuario';

  React.useEffect(() => {
    AxiosInstance.get('menu/')
      .then((res) => setMenu(res.data))
      .catch(() => setErrorMenu(true))
      .finally(() => setCargandoMenu(false));
  }, []);

  React.useEffect(() => {
    AxiosInstance.get('menu/')
      .then((res) => {
        console.log('MENU DEL BACKEND:', JSON.stringify(res.data, null, 2))
        setMenu(res.data)
      })
      .catch(() => setErrorMenu(true))
      .finally(() => setCargandoMenu(false))
  }, []);

  // Logo configurado en el backend (settings.LOGO_URL)
  React.useEffect(() => {
    AxiosInstance.get('')
      .then((res) => setLogoUrl(res.data.logo_url))
      .catch(() => {}); // si falla, se queda el SVG de respaldo
  }, []);

  // El mismo logo como icono de la pestaña del navegador
  React.useEffect(() => {
    if (!logoUrl) return;
    let link = document.querySelector("link[rel~='icon']");
    if (!link) {
      link = document.createElement('link');
      link.rel = 'icon';
      document.head.appendChild(link);
    }
    link.type = 'image/png';
    link.href = logoUrl;
  }, [logoUrl]);

  const changeOpenStatus = () => setOpen((prev) => !prev);
  const alternar = (id) => setAbiertos((prev) => ({ ...prev, [id]: !prev[id] }));

  const logoutUser = async () => {
    try {
      await AxiosInstance.post('logoutall/', {});
      localStorage.removeItem('Token');
      navigate('/');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    }
  };

  const myDrawer = (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Logo y nombre */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.25, px: 2.5, minHeight: ALTO_BARRA + 4, flexShrink: 0 }}>
        <LogoTeseracto src={logoUrl} size={36} />
        <Typography variant="h6" noWrap sx={{ fontWeight: 800, letterSpacing: 0.2 }}>
          Teseracto
        </Typography>
      </Box>

      {/* Menú */}
      <List sx={{ flexGrow: 1, overflow: 'auto', pt: 0.5 }}>
        {cargandoMenu && (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
            <CircularProgress size={22} sx={{ color: '#fff' }} />
          </Box>
        )}

        {errorMenu && (
          <Typography variant="body2" sx={{ p: 2, color: '#fff' }}>
            No se pudo cargar el menú.
          </Typography>
        )}

        {menu.map((item) => (
          <MenuNodo
            key={item.id}
            item={item}
            nivel={0}
            path={path}
            abiertos={abiertos}
            alternar={alternar}
            cerrarDrawer={() => setOpen(false)}
          />
        ))}
      </List>

      <Typography variant="caption" sx={{ px: 2.5, py: 2, opacity: 0.85, flexShrink: 0 }}>
        Versión {version}
      </Typography>
    </Box>
  );

  const paperDrawer = {
    width: drawerWidth,
    boxSizing: 'border-box',
    bgcolor: 'primary.main',
    color: '#fff',
    border: 'none',
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />

      {/* Barra superior: blanca, con buscador, notificaciones y usuario */}
      <AppBar
        position="fixed"
        elevation={0}
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          bgcolor: '#fff',
          color: 'text.primary',
          boxShadow: (t) => `0 1px 10px ${alpha(t.palette.primary.main, 0.1)}`,
        }}
      >
        <Toolbar sx={{ minHeight: ALTO_BARRA, gap: 1.5 }}>
          <IconButton
            edge="start"
            onClick={changeOpenStatus}
            sx={{ display: { xs: 'inline-flex', sm: 'none' }, color: 'primary.main' }}
            aria-label="Abrir menú"
          >
            <MenuIcon />
          </IconButton>

          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              flex: '1 1 auto',
              maxWidth: 440,
              height: 38,
              px: 1.75,
              borderRadius: '999px',
              bgcolor: (t) => lighten(t.palette.primary.main, 0.92),
              color: 'primary.main',
            }}
          >
            <SearchIcon fontSize="small" />
            <InputBase
              placeholder="Buscar en el sistema…"
              inputProps={{ 'aria-label': 'Buscar en el sistema' }}
              sx={{ flex: 1, fontSize: 13.5, color: 'text.primary' }}
            />
          </Box>

          <Box sx={{ flexGrow: 1 }} />

          <IconButton sx={{ color: 'primary.main' }} aria-label="Notificaciones">
            <Badge badgeContent={notificaciones} color="error">
              <NotificationsIcon fontSize="small" />
            </Badge>
          </IconButton>

          <Box
            component="button"
            type="button"
            onClick={(e) => setAnchorUsuario(e.currentTarget)}
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              p: 0,
              border: 'none',
              bgcolor: 'transparent',
              cursor: 'pointer',
              color: 'text.primary',
              font: 'inherit',
            }}
          >
            <Avatar sx={{ bgcolor: 'primary.main', width: 34, height: 34 }}>
              <PersonIcon fontSize="small" />
            </Avatar>
            <Typography sx={{ display: { xs: 'none', sm: 'block' }, fontWeight: 500, fontSize: 14 }}>
              {nombreUsuario}
            </Typography>
            <KeyboardArrowDownIcon fontSize="small" sx={{ color: 'primary.main' }} />
          </Box>

          <Menu
            anchorEl={anchorUsuario}
            open={Boolean(anchorUsuario)}
            onClose={() => setAnchorUsuario(null)}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
          >
            <MenuItem
              onClick={() => {
                setAnchorUsuario(null);
                logoutUser();
              }}
            >
              <ListItemIcon>
                <LogoutIcon fontSize="small" />
              </ListItemIcon>
              Cerrar sesión
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': paperDrawer,
        }}
      >
        {myDrawer}
      </Drawer>

      <Drawer
        variant="temporary"
        open={open}
        onClose={changeOpenStatus}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': paperDrawer,
        }}
      >
        {myDrawer}
      </Drawer>

      <Box
        component="main"
        sx={{ flexGrow: 1, minWidth: 0, p: { xs: 2, sm: 2.5 }, minHeight: '100vh', bgcolor: 'background.default' }}
      >
        <Toolbar sx={{ minHeight: ALTO_BARRA }} />
        {content}
      </Box>
    </Box>
  );
};

export default Navbar;