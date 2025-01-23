import { Main } from "../pages";
import { Donate } from "../pages";
import { Blog } from "../pages";
import { LetsPlay } from "../pages";
import { LogReg } from "../pages";
import { Profile } from "../pages";
export const privateRoutes = [
  { path: "/", component: <Main />, exact: true },
  { path: "/main", component: <Main />, exact: true },
  { path: "/donate", component: <Donate />, exact: true },
  { path: "/blog", component: <Blog />, exact: true },
  { path: "/letsPlay", component: <LetsPlay />, exact: true },
  { path: "/profile", component: <Profile />, exact: true },
];
export const publicRoutes = [
  { path: "/", component: <Main />, exact: true },
  { path: "/main", component: <Main />, exact: true },
  { path: "/donate", component: <Donate />, exact: true },
  { path: "/blog", component: <Blog />, exact: true },
  { path: "/letsPlay", component: <LetsPlay />, exact: true },
  { path: "/logReg", component: <LogReg />, exact: true },
];
