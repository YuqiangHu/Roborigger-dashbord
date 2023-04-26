import { combineReducers } from "redux";
import loginReducer from "./pages/auth/reducer"

const appReducer = combineReducers({
  auth: combineReducers({
    login: loginReducer,
  }),
});

export default appReducer