import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/auth/login";
import Register from "./pages/auth/register";
import HomePage from "./pages/homepage";
import Dashboard from "./pages/dashboard";
import AuthRoute from "./pages/auth/AuthRoute/index";
import React from "react";

function App() {
  return (
    <Router>
 
        <Routes>
		<Route
          path="/dashboard"
          element={
            <AuthRoute >
              <Dashboard />
            </AuthRoute>
          }
        />
		<Route
          path="/register"
          element={
            <AuthRoute>
              <Register />
            </AuthRoute>
          }
        />
		<Route
		  path="/login"
		  element={
			<AuthRoute>
			  <Login />
			</AuthRoute>
		  }
		/>
		

		  <Route exact path="/" element={<HomePage />} />
        </Routes>

    </Router>
  );
}

export default App;
