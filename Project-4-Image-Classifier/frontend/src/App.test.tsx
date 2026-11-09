import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('App', () => {
  it('renders the title and an initially disabled classify button', () => {
    render(<App />)
    expect(screen.getByText('Cat vs Dog Classifier')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /classify image/i })).toBeDisabled()
  })
})
