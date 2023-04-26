import {
    LOGIN_REQUESTING, LOGIN_SUCCESS, LOGIN_ERROR, USER_SET,
    USER_LOGOUT,
} from './constants'

const initialState = {
    requesting: false,
    messages: [],
    errors: [],
    loggedIn: false,
    userId: null,
    group: null,
}

const reducer = function loginReducer(state = initialState, action) {
    switch (action.type) {
        // Set the requesting flag and append a message to be shown
        case LOGIN_REQUESTING:
            return {
                ...state,
                requesting: true,
                messages: [{ body: 'Logging in...', time: new Date() }],
                errors: []
            }

        // Successful?  Reset the login state.
        case LOGIN_SUCCESS:
            return {
                errors: [],
                messages: [],
                requesting: false,
                loggedIn: true,
                ...state
            }

        // Append the error returned from our api
        // set the success and requesting flags to false
        case LOGIN_ERROR:
            let error
            error = action.error.statusText
            return {
                ...state,
                errors: state.errors.concat([
                    {
                        body: error,
                        time: new Date()
                    }
                ]),
                messages: [],
                requesting: false,
                loggedIn: false
            }
        case USER_SET:
            return {
                ...state,
                userId: action.token.user_id,
                group: action.token.group,
                loggedIn: true
            }

        // case USER_SET_PROFILE:
        //     return {
        //         ...state,
        //         profile: action.profile
        //     }

        case USER_LOGOUT:
            return initialState

        default:
            return state
    }
}

export default reducer