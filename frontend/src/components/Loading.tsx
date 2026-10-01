import { CircularProgress, Stack, Typography } from '@mui/material'

export default function Loading({ text = 'Loading...' }: { text?: string }) {
  return <Stack alignItems="center" justifyContent="center" spacing={1} sx={{ minHeight: 220 }}><CircularProgress /><Typography color="text.secondary">{text}</Typography></Stack>
}
