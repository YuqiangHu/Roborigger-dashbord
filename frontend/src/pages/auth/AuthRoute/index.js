import { useSelector } from "react-redux"
import { Navigate, Route } from "react-router"
import { getStoredTokenBool } from "./sagas"
import { useLocation } from 'react-router-dom'



const AuthRoute = ({ children }) => {
    const location = useLocation();
    console.log(location)
    const loggedIn = useSelector(state => state?.auth?.login?.loggedIn) || getStoredTokenBool()
    if (loggedIn) {
        if (location.pathname === "/login" || location.pathname === "/register") {
            return <Navigate to="/dashboard" />
        } 
        return children
    } else {
        if (location.pathname === "/login" || location.pathname === "/register") {
            return children
        }
        return <Navigate to="/login" />
    }
    
  };

export default AuthRoute