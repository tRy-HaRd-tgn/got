import styles from "./styles.module.scss";
import { Header, Footer, Video } from "../../components";
import { vector } from "../../imgs";
import { Swiper } from "swiper/react";
import { useNavigate } from "react-router-dom";
import { data } from "./data";
import { ProgressBar } from "../../components";
import "swiper/css";
import { useState } from "react";
export const Main = (props) => {
  const router = useNavigate();
  const [swiper, setSwiper] = useState(null);
  const [index, setIndex] = useState(0);
  return (
    <main className={styles.main}>
      <Header />
      <div className={styles.description}>
        <h1>TORTUGA GOT</h1>
        <p className={styles.descriptionP}>
          Здесь тебя ждут интриги, война и возможность вписать своё имя в
          историю Семи Королевств. Исследуй наши земли, выбирай свой путь,
          становись частью великого конфликта. Вступай в игру, где каждый твой
          шаг может изменить судьбу мира.
        </p>
        <button
          onClick={() => router("/letsPlay")}
          className={styles.descriptionBtn}
        >
          Начать свой путь
        </button>
      </div>
      <img src={vector} alt="" className={styles.devider} />
      <div className={styles.project}>
        <h3 style={{ marginBottom: "0px", marginTop: "5%" }}>Обзор проекта</h3>
        <div className={styles.videoWrapper}>
          <Swiper
            onSwiper={setSwiper}
            className={styles.swiper}
            spaceBetween={130}
            slidesPerView={1}
          >
            {data.map((value, index) =>
              Video({ key: index, index, value, swiper })
            )}
            <ProgressBar swiper={swiper} index={index} setIndex={setIndex} />
          </Swiper>
        </div>
      </div>
      <Footer />
    </main>
  );
};
