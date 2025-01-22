import styles from "./styles.module.scss";
import { user, calendar } from "../../imgs";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PostService from "../../services/PostService";
import { useState } from "react";

export const News = ({ header, img, text, id, author, data, url }) => {
  const navigator = useNavigate();
  const [image, setImage] = useState(null);
  useEffect(() => {
    try {
      setImage("http://localhost:8000"+img);
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
          <a target="_blank" className={styles.butn} href={url}>
            Подробнее
          </a>
        </div>
      </div>
    </div>
  );
};
