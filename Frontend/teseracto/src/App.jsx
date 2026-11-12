import { useState } from 'react'
import Home from './components/Home'
import Login from './components/Login'
import Navbar from './components/Navbar'
import {Routes, Route, useLocation} from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoutes'
import PasswordReset from './components/PasswordReset'
import PasswordResetRequest from './components/PasswordResetRequest'


import EmpresaList from './components/EmpresaList'
import EmpresaForm from './components/EmpresaForm'
import SucursalList from './components/SucursalList'
import SucursalForm from './components/SucursalForm'
import EmpresaConfiguracionList from './components/EmpresaConfiguracionList'
import EmpresaConfiguracionForm from './components/EmpresaConfiguracionForm'
import CategoriaList from './components/CategoriaList'
import CategoriaForm from './components/CategoriaForm'
import MarcaList from './components/MarcaList'
import MarcaForm from './components/MarcaForm'
import UnidadMedidaList from './components/UnidadMedidaList'
import UnidadMedidaForm from './components/UnidadMedidaForm'


function App() {
  const location = useLocation()
  const noNavbar = location.pathname === "/" || location.pathname.includes("password")

  return (
    <>
      {
        noNavbar ?
        <Routes>
            <Route path="/" element={<Login/>}/>
            <Route path="/request/password_reset" element={<PasswordResetRequest/>}/>
            <Route path="/password-reset/:token" element={<PasswordReset/>}/>
        </Routes>

        :

        <Navbar
        content={
          <Routes>
              <Route element={<ProtectedRoute />}>
                <Route path="/home" element={<Home />} />

                <Route path="/empresas" element={<EmpresaList />} />
                <Route path="/empresas/crear" element={<EmpresaForm />} />
                <Route path="/empresas/editar/:id" element={<EmpresaForm />} />

                <Route path="/empresas/:empresaId/sucursales" element={<SucursalList />} />
                <Route path="/empresas/:empresaId/sucursales/crear" element={<SucursalForm />} />
                <Route path="/empresas/:empresaId/sucursales/editar/:id" element={<SucursalForm />} />

                <Route path="/empresas/:empresaId/configuracion" element={<EmpresaConfiguracionList />} />
                <Route path="/empresas/:empresaId/configuracion/crear" element={<EmpresaConfiguracionForm />} />
                <Route path="/empresas/:empresaId/configuracion/editar/:id" element={<EmpresaConfiguracionForm />} />

                <Route path="/unidades_medida" element={<UnidadMedidaList />} />
                <Route path="/unidades_medida/crear" element={<UnidadMedidaForm />} />
                <Route path="/unidades_medida/editar/:id" element={<UnidadMedidaForm />} />

                <Route path="/categorias" element={<CategoriaList />} />
                <Route path="/categorias/crear" element={<CategoriaForm />} />
                <Route path="/categorias/editar/:id" element={<CategoriaForm />} />

                <Route path="/marcas" element={<MarcaList />} />
                <Route path="/marcas/crear" element={<MarcaForm />} />
                <Route path="/marcas/editar/:id" element={<MarcaForm />} />


              </Route>
            </Routes>

        }
      />
      }
    </>
  )
}

export default App