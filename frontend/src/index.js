import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import IndexReducer from "./index-reducer"
import IndexSagas from "./index-sagas";
import { applyMiddleware, createStore, compose } from "redux"
import { Provider } from "react-redux"
import createSagaMiddleware from "redux-saga"

const composeSetup = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const sagaMiddleware = createSagaMiddleware()

const store = createStore(
  IndexReducer, 
  composeSetup(applyMiddleware(sagaMiddleware)) // allows redux devtools to watch sagas
)

sagaMiddleware.run(IndexSagas)

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <Provider store={store}>
    <App />
  </Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
