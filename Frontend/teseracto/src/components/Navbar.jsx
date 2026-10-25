import * as React from 'react';
import {
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
  Divider,
} from '@mui/material';

import MenuIcon from '@mui/icons-material/Menu';
import LogoutIcon from '@mui/icons-material/Logout';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';

import { Link, useLocation, useNavigate } from 'react-router-dom';
import AxiosInstance from './AxiosInstance';
import { obtenerIcono } from './utils/iconos';
import { colores } from './utils/theme';

// Logo: cubo blanco sobre fondo azul (versión simplificada del de la pantalla de login)
const LogoTeseracto = ({ size = 30 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" aria-hidden="true">
    <path d="M24 3 43 13v22L24 45 5 35V13z" fill="#fff" />
    <path d="M24 24 43 13v22L24 45z" fill="#CFE0FB" />
    <path d="M24 24 5 13 24 3l19 10z" fill="#fff" />
    <path d="M24 24v21" stroke={colores.azul} strokeWidth="3" />
    <path d="M24 24 9 16M24 24l15-8" stroke={colores.azul} strokeWidth="3" />
  </svg>
);

// Estilo de los ítems del menú: píldora redondeada, azul claro al seleccionar
const estiloItem = (nivel) => ({
  mx: 1.5,
  my: 0.25,
  py: 1,
  pl: 1.5 + nivel * 2,
  borderRadius: '10px',
  color: 'text.secondary',
  '& .MuiListItemIcon-root': { minWidth: 38, color: 'inherit' },
  '& .MuiListItemText-primary': { fontSize: 14.5, fontWeight: 500 },
  '&:hover': { backgroundColor: colores.azulClaro, color: colores.azul },
  '&.Mui-selected': {
    backgroundColor: colores.azulClaro,
    color: colores.azul,
    '& .MuiListItemText-primary': { fontWeight: 700 },
    '&:hover': { backgroundColor: colores.azulClaro },
  },
});

// Item recursivo: si tiene hijos se despliega, si no, es un enlace.
const MenuNodo = ({ item, nivel, path, abiertos, alternar, cerrarDrawer }) => {
  const Icono = obtenerIcono(item.icono);

  if (item.hijos?.length > 0) {
    const abierto = !!abiertos[item.id];
    const hijoActivo = item.hijos.some((h) => h.url === path);
    return (
      <>
        <ListItem disablePadding>
          <ListItemButton
            onClick={() => alternar(item.id)}
            sx={{ ...estiloItem(nivel), ...(hijoActivo && { color: colores.azul }) }}
          >
            <ListItemIcon>
              <Icono />
            </ListItemIcon>
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
        selected={item.url === path}
        onClick={cerrarDrawer}
        sx={estiloItem(nivel)}
      >
        <ListItemIcon>
          <Icono />
        </ListItemIcon>
        <ListItemText primary={item.nombre} />
      </ListItemButton>
    </ListItem>
  );
};

const Navbar = (props) => {
  const { drawerWidth = 260, content } = props;

  const location = useLocation();
  const navigate = useNavigate();
  const path = location.pathname;

  const [open, setOpen] = React.useState(false);
  const [menu, setMenu] = React.useState([]);
  const [cargandoMenu, setCargandoMenu] = React.useState(true);
  const [errorMenu, setErrorMenu] = React.useState(false);
  const [abiertos, setAbiertos] = React.useState({});

  React.useEffect(() => {
    AxiosInstance.get('menu/')
      .then((res) => setMenu(res.data))
      .catch(() => setErrorMenu(true))
      .finally(() => setCargandoMenu(false));
  }, []);

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
    <>
      <Toolbar />

      <Box sx={{ overflow: 'auto', display: 'flex', flexDirection: 'column', flexGrow: 1, pt: 1.5 }}>
        <List sx={{ flexGrow: 1 }}>
          {cargandoMenu && (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
              <CircularProgress size={24} />
            </Box>
          )}

          {errorMenu && (
            <Typography variant="body2" color="error" sx={{ p: 2 }}>
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

        <Divider sx={{ mx: 2 }} />
        <List>
          <ListItem disablePadding>
            <ListItemButton
              onClick={() => {
                setOpen(false);
                logoutUser();
              }}
              sx={estiloItem(0)}
            >
              <ListItemIcon>
                <LogoutIcon />
              </ListItemIcon>
              <ListItemText primary="Cerrar sesión" />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </>
  );

  const paperDrawer = {
    width: drawerWidth,
    boxSizing: 'border-box',
    backgroundColor: '#fff',
    borderRight: `1px solid ${colores.borde}`,
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />

      <AppBar
        position="fixed"
        elevation={0}
        sx={{
          zIndex: (theme) => theme.zIndex.drawer + 1,
          background: `linear-gradient(90deg, ${colores.azulOscuro} 0%, ${colores.azul} 100%)`,
        }}
      >
        <Toolbar sx={{ gap: 1.5 }}>
          <IconButton
            color="inherit"
            edge="start"
            onClick={changeOpenStatus}
            sx={{ display: { xs: 'inline-flex', sm: 'none' } }}
            aria-label="Abrir menú"
          >
            <MenuIcon />
          </IconButton>

          <LogoTeseracto />
          <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 800, letterSpacing: 0.2 }}>
            Teseracto
          </Typography>
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

      <Box component="main" sx={{ flexGrow: 1, minWidth: 0, p: { xs: 2, sm: 3 }, minHeight: '100vh' }}>
        <Toolbar />
        {content}
      </Box>
    </Box>
  );
};

export default Navbar;