import React from 'react'
import ReactDOM from 'react-dom/client'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material'
import App from './App'
import './styles.css'

const theme=createTheme({palette:{primary:{main:'#8f78b6',contrastText:'#fff'},secondary:{main:'#7fa5b5'},background:{default:'#fcfbfe',paper:'#fff'},success:{main:'#7ca88c'},warning:{main:'#c6a36b'},error:{main:'#c47d7d'}},shape:{borderRadius:18},typography:{fontFamily:'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'},components:{MuiButton:{styleOverrides:{root:{borderRadius:12,textTransform:'none',fontWeight:700}}},MuiCard:{styleOverrides:{root:{border:'1px solid #eee8f3',boxShadow:'0 8px 28px rgba(78,65,91,.06)'}}},MuiTextField:{defaultProps:{size:'small'}},MuiOutlinedInput:{styleOverrides:{root:{borderRadius:12}}},MuiTableCell:{styleOverrides:{head:{fontWeight:800,background:'#faf8fc'}}}}})
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><ThemeProvider theme={theme}><CssBaseline/><App/></ThemeProvider></React.StrictMode>)
