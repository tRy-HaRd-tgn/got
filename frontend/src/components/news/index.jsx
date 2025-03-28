import styles from "./styles.module.scss";
import { user, calendar } from "../../imgs";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { API_URL2 } from "../../http";
export const News = ({ header, img, text, id, author, data, url }) => {
  const navigator = useNavigate();
  const [image, setImage] = useState(null);
  useEffect(() => {
    try {
      setImage(API_URL2 + img);
    } catch (e) {
      console.log(e);
    }
  }, []);
  return (
    <div className={styles.news}>
      <img className={styles.newsImg} src={image} alt="error" />
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
          <a
            style={{ marginTop: "0px" }}
            target="_blank"
            className={styles.butn}
            href={url}
          >
            Подробнее
          </a>
        </div>
      </div>
    </div>
  );
};
