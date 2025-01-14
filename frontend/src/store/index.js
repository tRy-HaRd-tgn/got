import { createStore, combineReducers } from "redux";
import { authReducer } from "./reducers/authReducer";
import { userReducer } from "./reducers/userReducer";

const rootReduce = combineReducers({
  auth: authReducer,
  user: userReducer,
});

export const store = createStore(
  rootReduce,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);
