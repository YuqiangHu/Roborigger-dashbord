import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CardMedia } from '@mui/material';
import RbLogo from '../../assets/images/Robo_logo.png';
import { Card } from '@mui/material';
import Layout from '../../components/layout';
import { useDispatch } from "react-redux";
import loginRequest from "./actions"

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        Rogorigger
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const theme = createTheme();

export default function SignIn() {
  const dispatch = useDispatch()
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log({
      email: data.get('email'),
      password: data.get('password'),
    });
    dispatch(loginRequest(data.get('email'), data.get('password')))
  };

  return (
    <ThemeProvider theme={theme}>
      <Layout title="Roborigger | Login" content="Login to your account">
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
           <Card
                raised
                sx={{
                    maxWidth: 220,
                    margin: "0 auto",
                    padding: "0.1em",
                }}
                >
                    <CardMedia
                    src={RbLogo} component="img" title="logo"   />
                    
            </Card>
            

      

            

            {/* <div>
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>

            </div> */}

            <Box sx={{marginTop:4,}} >
            <Typography component="h1" variant="h5">
            Sign in
          </Typography>
            </Box>

          {/* <Typography component="h1" variant="h5">
            Sign in
          </Typography> */}
        
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              id="submit"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            {/* <Grid >
              <Grid item align="center">
                <Link href="#" variant="body2" >
                  Forgot password?
                </Link>
              </Grid>
            </Grid> */}
            

            <Grid>
              <Grid item align="center">
                <Link href="/register" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>

            </Grid>
          </Box>
        </Box>
        <Copyright sx={{ mt: 8, mb: 4 }} />
      </Container>
      </Layout>
    </ThemeProvider>
  );
}