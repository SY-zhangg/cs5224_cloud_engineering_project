import { useContext, useEffect, useState } from 'react';
import { AccountContext } from './Account';
import Login from './Login';

import * as React from 'react';
import AccountCircleSharpIcon from '@mui/icons-material/AccountCircleSharp';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const Status = () => {
  const [status, setStatus] = useState(false);
  const { getSession, logout } = useContext(AccountContext);

  useEffect(() => {
    getSession()
      .then((session) => {
        console.log('Session: ', session);
        setStatus(true);
      })
      .catch((err) => {
        console.log('Session: ', err);
        setStatus(false);
      });
  }, [status]);

  const theme = createTheme();

  return (
    <div>
      {status ? (
        <div>
          <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <AccountCircleSharpIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            You are logged in !
          </Typography>
          <Box component="form" noValidate onSubmit={logout} sx={{ mt: 3 }}>
          <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Logout
            </Button>
          </Box>
        </Box>
        </Container>
        </ThemeProvider>
        </div>
      ) : (
        <Login />
      )}
    </div>
  );
};

export default Status;