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
import ConfiguracionList from './components/ConfiguracionList'
import ConfiguracionForm from './components/ConfiguracionForm'
import EmpresaConfiguracionList from './components/EmpresaConfiguracionList'
import EmpresaConfiguracionForm from './components/EmpresaConfiguracionForm'


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

                <Route path="/sucursales" element={<SucursalList />} />
                <Route path="/sucursales/crear" element={<SucursalForm />} />
                <Route path="/sucursales/editar/:id" element={<SucursalForm />} />

                <Route path="/configuraciones" element={<ConfiguracionList />} />
                <Route path="/configuraciones/crear" element={<ConfiguracionForm />} />
                <Route path="/configuraciones/editar/:id" element={<ConfiguracionForm />} />

                <Route path="/empresa_configuraciones" element={<EmpresaConfiguracionList />} />
                <Route path="/empresa_configuraciones/crear" element={<EmpresaConfiguracionForm />} />
                <Route path="/empresa_configuraciones/editar/:id" element={<EmpresaConfiguracionForm />} />
              </Route>
            </Routes>

        }
      />
      }
    </>
  )
}

export default App