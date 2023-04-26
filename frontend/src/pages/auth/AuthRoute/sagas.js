import { take, call, put, race, delay } from "redux-saga/effects"
// import { delay } from "redux-saga"

// Helper for api errors
import apiCall from "lib/apiCallSaga"

//Decode tokens to get expiry times
import jwtDecode from "jwt-decode"

// So that we can modify our User piece of state
import {
    userLogout,
    userSet,

} from "../actions"



import { USER_LOGOUT, USER_SET } from "../constants"

function setToken(token) {
    let currentToken = localStorage.getItem("token")
    let jsonTokens = JSON.parse(currentToken)
    jsonTokens.access = token.access
    localStorage.setItem("token", JSON.stringify(jsonTokens))
    return
}

export function getStoredTokenBool() {
    const storedToken = localStorage.getItem("token")
    const tokenBool = storedToken != null
    return tokenBool
}

function getStoredToken() {
    let tokens = localStorage.getItem("token")
    let jsonToken = JSON.parse(tokens)
    return jsonToken
}

function removeStoredToken() {
    localStorage.removeItem("token")
    return
}

function getApiParams() {
    let tokens = getStoredToken()
    let refresh = tokens.refresh
    let endpoint = "/api/token/refresh/"
    let apiCallParams = {
        method: "post",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ refresh })
    }
    let apiCallData = { endpoint, apiCallParams }
    return apiCallData
}

function* authorise(refresh) {
    try {
        let apiCallData = yield call(getApiParams)

        const token = yield call(
            apiCall,
            apiCallData.endpoint,
            apiCallData.apiCallParams
        )

        yield call(setToken, token)
        let decodedJWT = jwtDecode(token.access)
        yield put(userSet(decodedJWT))
        return token
    } catch (e) {
        yield call(removeStoredToken)
        yield put(userLogout(e))
        return null
    }
}

//Get new access token just prior to expiry.
function* authoriseLoop(token) {
    while (true) {
        const refresh = token != null
        token = yield call(authorise, refresh)
        if (token == null) return
        let storedToken = getStoredToken()
        let decodedToken = jwtDecode(storedToken.access)
        let tokenCallDelay = (decodedToken.exp * 1000 - Date.now()) * 0.9
        yield delay(tokenCallDelay)
    }
}

export default function* authentication() {
    while (true) {
        let storedToken = yield call(getStoredTokenBool)
        if (!storedToken) {
            yield take(USER_SET)
            storedToken = yield call(getStoredTokenBool)
        }
        const { signOutAction } = yield race({
            signOutAction: take(USER_LOGOUT),
            authLoop: call(authoriseLoop, storedToken)
        })
        if (signOutAction) {
            storedToken = null
            yield call(removeStoredToken)
        }
    }
}