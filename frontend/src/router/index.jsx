import {
  Main,
  Cancelled,
  Donate,
  Approved,
  Profile,
  LogReg,
  LetsPlay,
  Blog,
} from "../pages";
export const privateRoutes = [
  { path: "/", component: <Main />, exact: true },
  { path: "/main", component: <Main />, exact: true },
  { path: "/donate", component: <Donate />, exact: true },
  { path: "/blog", component: <Blog />, exact: true },
  { path: "/letsPlay", component: <LetsPlay />, exact: true },
  { path: "/profile", component: <Profile />, exact: true },
  { path: "/aproved", component: <Approved />, exact: true },
  { path: "/cancelled", component: <Cancelled />, exact: true },
];
export const publicRoutes = [
  { path: "/", component: <Main />, exact: true },
  { path: "/main", component: <Main />, exact: true },
  { path: "/donate", component: <Donate />, exact: true },
  { path: "/blog", component: <Blog />, exact: true },
  { path: "/letsPlay", component: <LetsPlay />, exact: true },
  { path: "/logReg", component: <LogReg />, exact: true },
  { path: "/aproved", component: <Approved />, exact: true },
  { path: "/cancelled", component: <Cancelled />, exact: true },
];
