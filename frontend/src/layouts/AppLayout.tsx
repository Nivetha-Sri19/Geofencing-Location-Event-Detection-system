import { useState } from 'react'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import {
  AppBar,
  Avatar,
  Box,
  Chip,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Toolbar,
  Typography,
  useMediaQuery,
  useTheme,
} from '@mui/material'

import DashboardRoundedIcon from '@mui/icons-material/DashboardRounded'
import FenceRoundedIcon from '@mui/icons-material/FenceRounded'
import DevicesOtherRoundedIcon from '@mui/icons-material/DevicesOtherRounded'
import LocationOnRoundedIcon from '@mui/icons-material/LocationOnRounded'
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded'
import HistoryRoundedIcon from '@mui/icons-material/HistoryRounded'
import FactCheckRoundedIcon from '@mui/icons-material/FactCheckRounded'
import MenuRoundedIcon from '@mui/icons-material/MenuRounded'
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded'

import { useAuth } from '../hooks/useAuth'

const width = 250

export default function AppLayout() {
  const [mobileOpen, setMobileOpen] = useState(false)

  const theme = useTheme()
  const mobile = useMediaQuery(theme.breakpoints.down('md'))

  const navigate = useNavigate()
  const location = useLocation()

  const { user, logout } = useAuth()

  const items = [
    {
      label: 'Dashboard',
      path: '/dashboard',
      icon: <DashboardRoundedIcon />,
    },
    {
      label: 'Geofences',
      path: '/geofences',
      icon: <FenceRoundedIcon />,
      roles: ['admin', 'operator', 'viewer'],
    },
    {
      label: 'Devices',
      path: '/devices',
      icon: <DevicesOtherRoundedIcon />,
    },
    {
      label: 'Live Map',
      path: '/map',
      icon: <LocationOnRoundedIcon />,
    },
    {
      label: 'Process Location',
      path: '/locations/process',
      icon: <LocationOnRoundedIcon />,
    },
    {
      label: 'Events & History',
      path: '/events',
      icon: <HistoryRoundedIcon />,
    },
    {
      label: 'Audit Logs',
      path: '/audit',
      icon: <FactCheckRoundedIcon />,
      roles: ['admin'],
    },
    {
      label: 'Users',
      path: '/users',
      icon: <PeopleRoundedIcon />,
      roles: ['admin'],
    },
  ]

  const visible = items.filter(
    (item) =>
      !item.roles ||
      (user && item.roles.includes(user.role)),
  )

  const drawer = (
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        background:
          'linear-gradient(180deg,#fffaff 0%,#f5f8ff 100%)',
      }}
    >
      <Stack sx={{ p: 2.5 }} spacing={0.5}>
        <Typography variant="h6" fontWeight={900}>
          Geo
          <span style={{ color: '#9b8acb' }}>
            Sense
          </span>
        </Typography>

        <Typography
          variant="caption"
          color="text.secondary"
        >
          Location event control center
        </Typography>
      </Stack>

      <Divider />

      <List sx={{ px: 1.2, py: 1.5 }}>
        {visible.map((item) => (
          <ListItemButton
            key={item.path}
            selected={location.pathname === item.path}
            onClick={() => {
              navigate(item.path)
              setMobileOpen(false)
            }}
            sx={{
              borderRadius: 2.5,
              mb: 0.5,
            }}
          >
            <ListItemIcon sx={{ minWidth: 40 }}>
              {item.icon}
            </ListItemIcon>

            <ListItemText
              primary={item.label}
            />
          </ListItemButton>
        ))}
      </List>

      <Box
        sx={{
          mt: 'auto',
          p: 2,
        }}
      >
        <Stack
          spacing={1.2}
          sx={{
            p: 1.5,
            borderRadius: 3,
            background: '#f4eff9',
          }}
        >
          <Stack
            direction="row"
            spacing={1.2}
            alignItems="center"
          >
            <Avatar
              sx={{
                bgcolor: '#c8b6e8',
                color: '#4d3f66',
              }}
            >
              {user?.username
                ?.slice(0, 1)
                .toUpperCase()}
            </Avatar>

            <Box sx={{ minWidth: 0 }}>
              <Typography
                fontWeight={700}
                noWrap
              >
                {user?.username}
              </Typography>

              <Chip
                size="small"
                label={user?.role}
                sx={{
                  textTransform: 'capitalize',
                }}
              />
            </Box>
          </Stack>

          <ListItemButton
            onClick={() => {
              logout()
              navigate('/login')
            }}
            sx={{
              borderRadius: 2,
            }}
          >
            <ListItemIcon sx={{ minWidth: 36 }}>
              <LogoutRoundedIcon />
            </ListItemIcon>

            <ListItemText primary="Sign out" />
          </ListItemButton>
        </Stack>
      </Box>
    </Box>
  )

  return (
    <Box
      sx={{
        display: 'flex',
        minHeight: '100vh',
        background: '#fcfbfe',
      }}
    >
      {mobile ? (
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={() => setMobileOpen(false)}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            '& .MuiDrawer-paper': {
              width,
            },
          }}
        >
          {drawer}
        </Drawer>
      ) : (
        <Drawer
          variant="permanent"
          sx={{
            width,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width,
              boxSizing: 'border-box',
              borderRight:
                '1px solid #eee8f3',
            },
          }}
        >
          {drawer}
        </Drawer>
      )}

      <Box
        sx={{
          flex: 1,
          minWidth: 0,
        }}
      >
        <AppBar
          position="sticky"
          elevation={0}
          color="inherit"
          sx={{
            borderBottom:
              '1px solid #eee8f3',
            background:
              'rgba(255,255,255,.84)',
            backdropFilter: 'blur(12px)',
          }}
        >
          <Toolbar>
            {mobile && (
              <IconButton
                onClick={() =>
                  setMobileOpen(true)
                }
                sx={{ mr: 1 }}
              >
                <MenuRoundedIcon />
              </IconButton>
            )}

            <Box sx={{ flex: 1 }} />

            <Chip
              label={`${user?.role ?? ''} access`}
              sx={{
                textTransform: 'capitalize',
                background: '#f0ecfa',
              }}
            />
          </Toolbar>
        </AppBar>

        <Box
          component="main"
          sx={{
            p: {
              xs: 2,
              md: 3.5,
            },
            maxWidth: 1600,
            mx: 'auto',
          }}
        >
          <Outlet />
        </Box>
      </Box>
    </Box>
  )
}