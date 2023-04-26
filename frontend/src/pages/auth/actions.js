import { LOGIN_REQUESTING, USER_LOGOUT, USER_SET } from './constants'

// In order to perform an action of type LOGIN_REQUESTING
// we need an email and password

export const userLogout = () => ({
    type: USER_LOGOUT
})

const loginRequest = function loginRequest(email, password) {
    return {
        type: LOGIN_REQUESTING,
        email,
        password
    }
}

export const userSet = token => ({
    type: USER_SET,
    token
})

// Since it's the only one here
export default loginRequest