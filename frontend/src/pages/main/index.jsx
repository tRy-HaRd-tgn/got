import styles from "./styles.module.scss";
import React from "react";
import { Header, Footer, Video, ProgressBar } from "../../components";
import { Swiper } from "swiper/react";
import { useNavigate } from "react-router-dom";
import { data, data2 } from "./data";
import { header, about, vector } from "../../imgs";
import "swiper/css";
import { useState } from "react";
export const Main = () => {
  const router = useNavigate();
  const [swiper, setSwiper] = useState(null);
  const [index, setIndex] = useState(0);
  return (
    <main className={styles.main}>
      <Header />
      <div className={styles.description}>
        <img className={styles.img} src={header} alt="" />
        <h1>TORTUGA GOT</h1>
        <p className={styles.descriptionP}>{data2.text}</p>
        <button
          onClick={() => router("/letsPlay")}
          className={styles.descriptionBtn}
        >
          Начать свой путь
        </button>
      </div>
      <img src={vector} alt="" className={styles.devider} />
      <div className={styles.project}>
        <img className={styles.img} src={about} alt="" />
        <h3 style={{ marginBottom: "0px", marginTop: "5%" }}>Обзор проекта</h3>
        <div className={styles.videoWrapper}>
          <Swiper
            onSwiper={setSwiper}
            className={styles.swiper}
            spaceBetween={130}
            slidesPerView={1}
          >
            {data.map((value) => (
              <React.Fragment key={value.id}>
                {Video({ value: value, swiper })}
              </React.Fragment>
            ))}
            <ProgressBar swiper={swiper} index={index} setIndex={setIndex} />
          </Swiper>
        </div>
      </div>
      <Footer />
    </main>
  );
};
