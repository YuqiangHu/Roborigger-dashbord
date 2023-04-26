import * as React from "react";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import RbLogo from "../../assets/images/Robo_logo.png";
import { Card } from "@mui/material";
import { CardMedia } from "@mui/material";
import Layout from "../../components/layout";
import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";
import { useState } from "react";
import { apiPost } from "lib/apiCall";
import { useNavigate } from "react-router-dom";

function Copyright(props) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      {...props}
    >
      {"Copyright © "}
      <Link color="inherit" href="https://mui.com/">
        Roborigger
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

const theme = createTheme();

export default function SignUp() {
  const navigate = useNavigate();

  const { loggedIn } = useSelector((state) => state?.auth?.login);
  console.log(loggedIn);
  const [errorMsg, setErrorMsg] = useState(null);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });

  const onChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  const { first_name, last_name, email, password } = formData;

  const onSubmit = (e) => {
    e.preventDefault();
    const { first_name, last_name, email, password } = formData;
    apiPost("/api/users/register", {
      first_name,
      last_name,
      email,
      password,
    })
      .then((res) => {
        if (res.status === 400) {
          setErrorMsg("Password is too simple or email already exits");
        }
        if (res?.first_name) {
          navigate("/login");
          setErrorMsg(null);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  if (loggedIn) return <Navigate to="/dashboard" />;

  return (
    <ThemeProvider theme={theme}>
      <Layout title="Roborigger | Register" content="Register for an account">
        <Container component="main" maxWidth="xs">
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
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
              <CardMedia src={RbLogo} component="img" title="logo" />
            </Card>
            <Box sx={{ marginTop: 4 }}>
              <Typography component="h1" variant="h5">
                Sign up
              </Typography>
            </Box>
            <Box component="form" noValidate onSubmit={onSubmit} sx={{ mt: 3 }}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    autoComplete="given-name"
                    name="first_name"
                    value={first_name}
                    onChange={onChange}
                    required
                    fullWidth
                    id="firstName"
                    label="First Name"
                    autoFocus
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    id="lastName"
                    label="Last Name"
                    name="last_name"
                    value={last_name}
                    onChange={onChange}
                    autoComplete="family-name"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    value={email}
                    onChange={onChange}
                    autoComplete="email"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    name="password"
                    value={password}
                    onChange={onChange}
                    label="Password"
                    type="password"
                    id="password"
                    helperText="Password must be at least 8 characters, can not be fully digits"
                    autoComplete="new-password"
                  />
                </Grid>
                {errorMsg && (
                  <Grid item xs={12}>
                    <Typography variant="caption" style={{color: "red"}}>{errorMsg}</Typography>
                  </Grid>
                )}
              </Grid>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                onClick={onSubmit}
                id="submit"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign Up
              </Button>
              <Grid container justifyContent="flex-end">
                <Grid item xs align="center">
                  <Link href="/login" variant="body2">
                    Already have an account? Sign in
                  </Link>
                </Grid>
              </Grid>
            </Box>
          </Box>
          <Copyright sx={{ mt: 5 }} />
        </Container>
      </Layout>
    </ThemeProvider>
  );
}
