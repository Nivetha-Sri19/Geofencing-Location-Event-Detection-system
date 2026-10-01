import { Stack, Typography } from '@mui/material'
import type { ReactNode } from 'react'

export default function PageHeader({ title, subtitle, action }: { title: string; subtitle?: string; action?: ReactNode }) {
  return <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" alignItems={{ xs: 'flex-start', md: 'center' }} spacing={2} sx={{ mb: 3 }}><Stack spacing={0.5}><Typography variant="h4" fontWeight={800}>{title}</Typography>{subtitle && <Typography color="text.secondary">{subtitle}</Typography>}</Stack>{action}</Stack>
}
