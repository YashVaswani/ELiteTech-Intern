import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `px-3 py-2 rounded-md text-sm font-medium ${
    isActive ? 'bg-brand-600 text-white' : 'text-gray-600 hover:bg-gray-100'
  }`

export function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  if (!user) return null

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
        <span className="text-lg font-semibold text-brand-700">🥗 Calorie Tracker</span>
        <div className="flex items-center gap-2">
          <NavLink to="/" end className={linkClass}>
            Dashboard
          </NavLink>
          <NavLink to="/scan" className={linkClass}>
            Scan Food
          </NavLink>
          <NavLink to="/foods" className={linkClass}>
            Food Database
          </NavLink>
          <button
            onClick={() => {
              logout()
              navigate('/login')
            }}
            className="px-3 py-2 text-sm font-medium text-gray-500 hover:text-gray-800"
          >
            Log out
          </button>
        </div>
      </div>
    </nav>
  )
}
