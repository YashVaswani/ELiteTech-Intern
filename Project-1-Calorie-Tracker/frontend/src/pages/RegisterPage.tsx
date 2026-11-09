import { Link, useNavigate } from 'react-router-dom'
import { AuthForm } from '../components/AuthForm'
import { useAuth } from '../hooks/useAuth'

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()

  return (
    <AuthForm
      title="Create your account"
      submitLabel="Sign up"
      onSubmit={async (email, password) => {
        await register(email, password)
        navigate('/')
      }}
      footer={
        <>
          Already have an account?{' '}
          <Link to="/login" className="font-medium text-brand-600 hover:underline">
            Log in
          </Link>
        </>
      }
    />
  )
}
