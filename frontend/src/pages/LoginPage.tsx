import { useState } from 'react'
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Stack,
  TextField,
  Typography,
} from '@mui/material'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { apiError } from '../api/client'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [username, setUsername] = useState('Nivetha01')
  const [password, setPassword] = useState('Nivetha@123')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()

    setError('')

    if (!username.trim()) {
      setError('Username is required.')
      return
    }

    if (!password) {
      setError('Password is required.')
      return
    }

    setBusy(true)

    try {
      await login(username.trim(), password)

      navigate('/dashboard', {
        replace: true,
      })
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'grid',
        placeItems: 'center',
        p: 2,
        background:
          'radial-gradient(circle at 15% 20%, #f7e9f1 0, transparent 28%), radial-gradient(circle at 90% 80%, #e8f0fb 0, transparent 32%), #fcfbfe',
      }}
    >
      <Card
        sx={{
          width: '100%',
          maxWidth: 440,
          borderRadius: 5,
          boxShadow:
            '0 24px 70px rgba(87, 71, 107, .12)',
        }}
      >
        <CardContent
          sx={{
            p: {
              xs: 3,
              sm: 5,
            },
          }}
        >
          <Stack spacing={3}>

            {/* Branding */}
            <Stack
              alignItems="center"
              spacing={1}
            >
              <Box
                sx={{
                  width: 58,
                  height: 58,
                  display: 'grid',
                  placeItems: 'center',
                  borderRadius: 3,
                  background:
                    'linear-gradient(135deg, #eadff5, #dceffc)',
                  color: '#765c91',
                  fontSize: 28,
                }}
              >
                ⌖
              </Box>

              <Typography
                variant="h5"
                fontWeight={900}
              >
                SyncSphere
              </Typography>

              <Typography
                variant="body2"
                color="text.secondary"
              >
                OFFLINE-FIRST CONTROL
              </Typography>

              <Typography
                variant="h4"
                fontWeight={900}
                sx={{ mt: 1 }}
              >
                Welcome back.
              </Typography>

              <Typography
                color="text.secondary"
                textAlign="center"
              >
                Enter the control center and manage
                your location events.
              </Typography>
            </Stack>

            {/* Error */}
            {error && (
              <Alert severity="error">
                {error}
              </Alert>
            )}

            {/* Login form */}
            <Box
              component="form"
              onSubmit={submit}
              noValidate
            >
              <Stack spacing={2}>

                <TextField
                  label="Username"
                  type="text"
                  value={username}
                  onChange={(e) =>
                    setUsername(e.target.value)
                  }
                  fullWidth
                  autoFocus
                  required
                  autoComplete="username"
                  inputProps={{
                    spellCheck: false,
                  }}
                />

                <TextField
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  fullWidth
                  required
                  autoComplete="current-password"
                />

                <Button
                  type="submit"
                  variant="contained"
                  size="large"
                  disabled={
                    busy ||
                    !username.trim() ||
                    !password
                  }
                  sx={{
                    borderRadius: 2.5,
                    py: 1.3,
                    fontWeight: 700,
                  }}
                >
                  {busy
                    ? 'Signing in...'
                    : 'Sign in'}
                </Button>

              </Stack>
            </Box>

            <Typography
              variant="caption"
              color="text.secondary"
              textAlign="center"
            >
              Connected to the live FastAPI backend.
            </Typography>

          </Stack>
        </CardContent>
      </Card>
    </Box>
  )
}