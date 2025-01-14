import styles from "./styles.module.scss";
import { vk, ds, yt, tg } from "../../imgs";
export const NavBar = (props) => {
  return (
    <div className={styles.navbar}>
      <ul className={styles.list}>
        <li className={styles.li}>
          <a href="https://vk.com/tortugagot">
            <img src={vk} alt="error" />
          </a>
        </li>
        <li className={styles.li}>
          <a href="https://t.me/tortugagot">
            <img src={tg} alt="error" />
          </a>
        </li>
        <li className={styles.li}>
          <a href="https://discord.gg/hRq59KCcCS">
            <img src={ds} alt="error" />
          </a>
        </li>
        <li className={styles.li}>
          <a href="https://youtube.com/@tortuga4057?si=V7y69ocUy9osyQNx">
            <img src={yt} alt="error" />
          </a>
        </li>
      </ul>
    </div>
  );
};
