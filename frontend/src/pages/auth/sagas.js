import { take, fork, cancel, call, put, cancelled } from 'redux-saga/effects'

// Helper for api errors
import { apiPost } from 'lib/apiCallSaga'

import jwtDecode from 'jwt-decode'

// Our login constants
import { LOGIN_REQUESTING, LOGIN_SUCCESS, LOGIN_ERROR } from './constants'

// So that we can modify our User piece of state
import { userSet, userLogout } from './actions'

import { USER_LOGOUT } from './constants'

function* logout() {
    // dispatches the USER_LOGOUT action
    yield put(userLogout())
    // remove our token
    localStorage.removeItem('token')
}

function* loginFlow(email, password) {
    let token
    let apiCallParams = { email, password }
    try {
        token = yield call(apiPost, "/api/token/", apiCallParams)
        let accessTokenDecoded = jwtDecode(token.access)
        localStorage.setItem('token', JSON.stringify(token))
        yield put(userSet(accessTokenDecoded))
        yield put({ type: LOGIN_SUCCESS })
    } catch (error) {
        // error? send it to redux
        yield put({ type: LOGIN_ERROR, error })
    } finally {
        // No matter what, if our `forked` `task` was cancelled
        // we will then just redirect them to login
        if (yield cancelled()) {
        }
    }

    // return the token for health and wealth
    return token
}

// Our watcher (saga).  It will watch for many actions.
function* loginWatcher() {
    while (true) {
        //sit here and WAIT for this LOGIN_REQUESTING action and take USer/pass from the payload.
        const { email, password } = yield take(LOGIN_REQUESTING)
        // pass the email and password to our loginFlow() without pausing execution (fork)
        const task = yield fork(loginFlow, email, password)
        //wait for a logout or login error action
        const action = yield take([USER_LOGOUT, LOGIN_ERROR])
        //if we get a logout action, cancel the a pending login attempt
        if (action.type === USER_LOGOUT) yield cancel(task)
        yield call(logout)
    }
}

export default loginWatcher