import { setContext } from "redux-saga/effects"

import LoginSaga from "pages/auth/sagas"
import AuthSaga from "pages/auth/AuthRoute/sagas"

import { all } from "redux-saga/effects"


export default function* IndexSaga() {

    yield all([
        LoginSaga(),
        AuthSaga()
    ])
}