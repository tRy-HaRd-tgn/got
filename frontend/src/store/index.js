import { createStore, combineReducers } from "redux";
import { authReducer } from "./reducers/authReducer";
import { userReducer } from "./reducers/userReducer";
import { newsReducer } from "./reducers/newsReducer";
import { menuReducer } from "./reducers/menuReducer";

const rootReduce = combineReducers({
  auth: authReducer,
  user: userReducer,
  news: newsReducer,
  menu: menuReducer,
});

export const store = createStore(
  rootReduce,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);
