import { useEffect, useState } from 'react'
import {
  Alert,
  Button,
  Card,
  CardContent,
  Chip,
  Grid,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from '@mui/material'

import { devicesApi } from '../api/devices'
import { locationsApi } from '../api/locations'
import { apiError } from '../api/client'
import type {
  Device,
  LocationProcessingResponse,
} from '../types/api'
import PageHeader from '../components/PageHeader'
import Loading from '../components/Loading'

function localDateTimeWithOffset() {
  const d = new Date()

  const pad = (n: number) => String(n).padStart(2, '0')

  const offset = -d.getTimezoneOffset()
  const sign = offset >= 0 ? '+' : '-'
  const abs = Math.abs(offset)

  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(
    d.getDate(),
  )}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(
    d.getSeconds(),
  )}${sign}${pad(Math.floor(abs / 60))}:${pad(abs % 60)}`
}

export default function LocationProcessPage() {
  const [devices, setDevices] = useState<Device[]>([])
  const [deviceId, setDeviceId] = useState('')
  const [lat, setLat] = useState('13.0827')
  const [lon, setLon] = useState('80.2707')
  const [timestamp, setTimestamp] = useState(
    localDateTimeWithOffset(),
  )

  const [result, setResult] =
    useState<LocationProcessingResponse | null>(null)

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    devicesApi
      .list()
      .then((data) => {
        setDevices(data)

        if (data[0]) {
          setDeviceId(String(data[0].id))
        }
      })
      .catch((e) => {
        setError(apiError(e))
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  const submit = async () => {
    if (!deviceId) {
      setError('Please select a device.')
      return
    }

    if (!lat || !lon) {
      setError('Latitude and longitude are required.')
      return
    }

    if (Number(lat) < -90 || Number(lat) > 90) {
      setError('Latitude must be between -90 and 90.')
      return
    }

    if (Number(lon) < -180 || Number(lon) > 180) {
      setError('Longitude must be between -180 and 180.')
      return
    }

    if (!timestamp.includes('+') && !timestamp.endsWith('Z')) {
      setError(
        'Timestamp must include timezone information, for example +05:30.',
      )
      return
    }

    setBusy(true)
    setError('')
    setResult(null)

    try {
      const data = await locationsApi.process({
        device_id: Number(deviceId),
        latitude: Number(lat),
        longitude: Number(lon),
        timestamp,
      })

      setResult(data)
    } catch (e) {
      setError(apiError(e))
    } finally {
      setBusy(false)
    }
  }

  const resetTimestamp = () => {
    setTimestamp(localDateTimeWithOffset())
  }

  if (loading) {
    return <Loading text="Loading active devices..." />
  }

  return (
    <>
      <PageHeader
        title="Process Location"
        subtitle="Send a timestamped GPS reading to the live geofencing engine."
      />

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={2.5}>
        {/* GPS Submission */}
        <Grid size={{ xs: 12, md: 7 }}>
          <Card>
            <CardContent>
              <Stack spacing={2.2}>
                <Typography variant="h6" fontWeight={800}>
                  GPS submission
                </Typography>

                <Select
                  value={deviceId}
                  displayEmpty
                  fullWidth
                  onChange={(e) => setDeviceId(e.target.value)}
                >
                  <MenuItem value="">
                    Select device
                  </MenuItem>

                  {devices
                    .filter((device) => device.is_active)
                    .map((device) => (
                      <MenuItem
                        key={device.id}
                        value={device.id}
                      >
                        #{device.id} · {device.name}
                      </MenuItem>
                    ))}
                </Select>

                <Stack
                  direction={{ xs: 'column', sm: 'row' }}
                  spacing={2}
                >
                  <TextField
                    fullWidth
                    label="Latitude"
                    type="number"
                    value={lat}
                    onChange={(e) => setLat(e.target.value)}
                    inputProps={{
                      min: -90,
                      max: 90,
                      step: 'any',
                    }}
                  />

                  <TextField
                    fullWidth
                    label="Longitude"
                    type="number"
                    value={lon}
                    onChange={(e) => setLon(e.target.value)}
                    inputProps={{
                      min: -180,
                      max: 180,
                      step: 'any',
                    }}
                  />
                </Stack>

                <TextField
                  label="Timestamp with timezone"
                  value={timestamp}
                  onChange={(e) => setTimestamp(e.target.value)}
                  helperText="Example: 2026-09-30T11:40:00+05:30"
                  fullWidth
                />

                <Stack
                  direction={{ xs: 'column', sm: 'row' }}
                  spacing={1.5}
                >
                  <Button
                    variant="outlined"
                    onClick={resetTimestamp}
                    disabled={busy}
                  >
                    Use current time
                  </Button>

                  <Button
                    variant="contained"
                    size="large"
                    disabled={!deviceId || busy}
                    onClick={submit}
                    sx={{
                      flex: 1,
                      borderRadius: 2.5,
                      py: 1.3,
                    }}
                  >
                    {busy
                      ? 'Processing...'
                      : '📍 Process location'}
                  </Button>
                </Stack>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Engine Result */}
        <Grid size={{ xs: 12, md: 5 }}>
          <Card
            sx={{
              background: '#f7f1fa',
              minHeight: 260,
            }}
          >
            <CardContent>
              <Stack spacing={1.5}>
                <Typography
                  variant="h6"
                  fontWeight={800}
                >
                  Engine result
                </Typography>

                {!result ? (
                  <Typography color="text.secondary">
                    Submit a location to see geofence
                    transitions returned by the backend.
                  </Typography>
                ) : (
                  <>
                    <Stack
                      direction="row"
                      spacing={1}
                      flexWrap="wrap"
                      useFlexGap
                    >
                      <Chip
                        label={`Location #${result.location_event_id}`}
                        size="small"
                      />

                      <Chip
                        label={`Device #${result.device_id}`}
                        size="small"
                      />
                    </Stack>

                    <Typography
                      variant="body2"
                      fontWeight={600}
                    >
                      Coordinates
                    </Typography>

                    <Typography variant="body2">
                      {result.latitude.toFixed(6)},{' '}
                      {result.longitude.toFixed(6)}
                    </Typography>

                    <Stack spacing={1}>
                      {result.events.length === 0 ? (
                        <Typography color="text.secondary">
                          No event rule fired for this
                          location.
                        </Typography>
                      ) : (
                        result.events.map((event, index) => (
                          <Stack
                            key={index}
                            sx={{
                              p: 1.4,
                              borderRadius: 2.5,
                              background: '#fff',
                            }}
                          >
                            <Stack
                              direction="row"
                              justifyContent="space-between"
                              alignItems="center"
                              spacing={1}
                            >
                              <Typography
                                fontWeight={800}
                                sx={{
                                  textTransform:
                                    'capitalize',
                                }}
                              >
                                {event.event_type}
                              </Typography>

                              <Chip
                                size="small"
                                label={`${event.previous_state} → ${event.current_state}`}
                              />
                            </Stack>

                            <Typography
                              variant="body2"
                              sx={{ mt: 0.5 }}
                            >
                              {event.geofence_name}
                            </Typography>
                          </Stack>
                        ))
                      )}
                    </Stack>
                  </>
                )}
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </>
  )
}