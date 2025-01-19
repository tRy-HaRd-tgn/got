import { createStore, combineReducers } from "redux";
import { authReducer } from "./reducers/authReducer";
import { userReducer } from "./reducers/userReducer";
import { newsReducer } from "./reducers/newsReducer";

const rootReduce = combineReducers({
  auth: authReducer,
  user: userReducer,
  news: newsReducer,
});

export const store = createStore(
  rootReduce,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);
