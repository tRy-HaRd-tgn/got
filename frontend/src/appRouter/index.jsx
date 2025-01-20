import { useSelector } from "react-redux";
import { privateRoutes, publicRoutes } from "../router";
import { Routes, Route } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useEffect } from "react";
import UserService from "../services/UserService";
export const AppRouter = () => {
  const auth = useSelector((state) => state.auth.isAuth);
  const dispatch = useDispatch();
  const setAuth = (temp) => {
    dispatch({ type: "SET_AUTH", isAuth: temp });
  };
  const setNickName = (temp) => {
    dispatch({ type: "SET_NICKNAME", nickname: temp });
  };
  const setDonate = (temp) => {
    dispatch({ type: "SET_DONATE", donate: temp });
  };
  const setRegDate = (temp) => {
    dispatch({ type: "SET_REGDATE", regDate: temp });
  };
  const setEmail = (temp) => {
    dispatch({ type: "SET_EMAIL", email: temp });
  };
  const configureStore = async () => {
    const responce = await UserService.getProfile();
    setNickName(responce.data.login);
    setDonate(responce.data.balance);
    setRegDate(responce.data.created_at.split("T")[0]);
    setEmail(responce.data.email);
  };
  const checkAuth = async () => {
    try {
      const response = await UserService.checkAuth();
      setAuth(true);
      configureStore();
    } catch (e) {
      console.log(e.responce?.data?.message);
    }
  };
  useEffect(() => {
    if (localStorage.getItem("token")) checkAuth();
  }, []);
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
