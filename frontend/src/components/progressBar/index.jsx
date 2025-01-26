import { use } from "react";
import styles from "./styles.module.scss";
import { useEffect } from "react";
export const ProgressBar = ({ swiper, index, setIndex }) => {
  return (
    <div className={styles.progressBar}>
      {new Array(3).fill(0).map((_, i) => (
        <div
          key={i}
          id={i}
          className={i != index ? styles.bar : styles.active}
          onClick={() => {
            setIndex(i);
            swiper.slideTo(i);
          }}
        />
      ))}
    </div>
  );
};
