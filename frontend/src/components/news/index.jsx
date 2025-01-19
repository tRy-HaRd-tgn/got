import styles from "./styles.module.scss";
import { newsComp } from "../../imgs";
import { user, calendar } from "../../imgs";
import { useNavigate } from "react-router-dom";
export const News = ({ header, text, author, data, url }) => {
  const navigator = useNavigate();
  return (
    <div className={styles.news}>
      <img className={styles.newsImg} src={newsComp} alt="error" />
      <div className={styles.newsRight}>
        <h2>{header}</h2>
        <p className={styles.newsRightP}>{text}</p>
        <div className={styles.newsFooter}>
          <div className={styles.newsFooterWrapper}>
            <div className={styles.flex}>
              <img style={{ marginRight: "10px" }} src={user} alt="error" />
              <p className={styles.p}>{author}</p>
            </div>
            <div className={styles.flex}>
              <img style={{ marginRight: "10px" }} src={calendar} alt="error" />
              <p className={styles.p}>{data}</p>
            </div>
          </div>
          <a target="_blank" className={styles.butn} href={url}>Подробнее</a>
        </div>
      </div>
    </div>
  );
};
