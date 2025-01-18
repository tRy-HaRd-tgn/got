import { useSelector } from "react-redux";
import { privateRoutes, publicRoutes } from "../router";
import { Routes, Route } from "react-router-dom";
export const AppRouter = () => {
  const auth = useSelector((state) => state.auth.isAuth);
  return (
    <Routes>
      {auth
        ? privateRoutes.map((route, index) => (
            <Route
              key={index}
              element={route.component}
              path={route.path}
              exact={route.exact}
            />
          ))
        : publicRoutes.map((route, index) => (
            <Route
              key={index}
              element={route.component}
              path={route.path}
              exact={route.exact}
            />
          ))}
    </Routes>
  );
};
