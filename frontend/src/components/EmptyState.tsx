import { Stack, Typography } from '@mui/material'
import InboxOutlinedIcon from '@mui/icons-material/InboxOutlined'
export default function EmptyState({ text }: { text: string }) { return <Stack alignItems="center" spacing={1} sx={{ py: 7, color: 'text.secondary' }}><InboxOutlinedIcon fontSize="large"/><Typography>{text}</Typography></Stack> }
