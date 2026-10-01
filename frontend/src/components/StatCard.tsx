import { Card, CardContent, Stack, Typography } from '@mui/material'
import type { ReactNode } from 'react'

export default function StatCard({ label, value, icon, tone }: { label: string; value: number | string; icon: ReactNode; tone: string }) {
  return <Card sx={{ height: '100%', background: tone }}><CardContent><Stack direction="row" justifyContent="space-between" alignItems="center"><Stack spacing={0.5}><Typography variant="body2" color="text.secondary">{label}</Typography><Typography variant="h4" fontWeight={800}>{value}</Typography></Stack><Stack className="stat-icon">{icon}</Stack></Stack></CardContent></Card>
}
