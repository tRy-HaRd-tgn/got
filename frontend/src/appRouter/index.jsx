import { privateRoutes, publicRoutes } from "../router";
import { Routes, Route, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";

import { useEffect } from "react";
import UserService from "../services/UserService";
import { API_URL2 } from "../http";
import SkinService from "../services/SkinService";
export const AppRouter = () => {
  const router = useNavigate();
  const navigator = useNavigate();
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
  const setProfilePhoto = (temp) => {
    dispatch({ type: "SET_PROFILE_PHOTO", profilePhoto: temp });
  };
  const setSkin = (temp) => {
    dispatch({ type: "SET_SKIN", skin: temp });
  };
  const setChoise = (temp) => dispatch({ type: "SET_CHOISE", choise: temp });
  const configureStore = async () => {
    const responce = await UserService.getProfile();
    setNickName(responce.data.login);
    setDonate(responce.data.balance);
    setRegDate(responce.data.created_at.split("T")[0]);
    setEmail(responce.data.email);
    const responce2 = await SkinService.getAvatar();
    setProfilePhoto(API_URL2 + responce2.data);
    const responce3 = await SkinService.getSkin();
    setSkin(API_URL2 + responce3.data);
  };
  const checkAuth = async () => {
    try {
      const response = await UserService.checkAuth();
      setAuth(true);
      configureStore();
    } catch (e) {
      try {
        const responce = await UserService.logout();
        console.log(responce);
        localStorage.removeItem("token");
        setAuth(false);
        router("/main");
        location.reload();
      } catch (e) {
        console.log(e.responce?.data?.message);
      }
      console.log(e.responce?.data?.message);
    }
  };
  useEffect(() => {
    const href = window.location.href;
    if (
      !href.includes("login") &&
      !href.includes("register") &&
      !href.includes("donate") &&
      !href.includes("blog") &&
      !href.includes("letsPlay") &&
      !href.includes("logReg") &&
      !href.includes("profile") &&
      !href.includes("fk-verify.html")
    ) {
      navigator("/main");
      setChoise("главная");
    }
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
