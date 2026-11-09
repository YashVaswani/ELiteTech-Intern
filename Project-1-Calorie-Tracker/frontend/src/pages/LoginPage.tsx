import { Link, useNavigate } from 'react-router-dom'
import { AuthForm } from '../components/AuthForm'
import { useAuth } from '../hooks/useAuth'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()

  return (
    <AuthForm
      title="Log in"
      submitLabel="Log in"
      onSubmit={async (email, password) => {
        await login(email, password)
        navigate('/')
      }}
      footer={
        <>
          No account?{' '}
          <Link to="/register" className="font-medium text-brand-600 hover:underline">
            Sign up
          </Link>
        </>
      }
    />
  )
}
