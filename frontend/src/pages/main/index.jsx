import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector } from "../../imgs";
import { Swiper, SwiperSlide } from "swiper/react";
import { ProgressBar } from "../../components";
import "swiper/css";
export const Main = (props) => {
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
        <button className={styles.descriptionBtn}>Начать свой путь</button>
      </div>
      <img src={vector} alt="" className={styles.devider} />
      <div className={styles.project}>
        <h3>Обзор проекта</h3>
        <Swiper
          className={styles.swiper}
          spaceBetween={150}
          slidesPerView={1}
          onSlideChange={() => console.log("slide change")}
          onSwiper={(swiper) => console.log(swiper)}
        >
          <SwiperSlide style={{ backgroundColor: "red" }}>
            <ProgressBar index={0}/>
          </SwiperSlide>
          <SwiperSlide style={{ backgroundColor: "green" }}>
            <ProgressBar index={1}/>
          </SwiperSlide>
          <SwiperSlide style={{ backgroundColor: "blue" }}>
            <ProgressBar index={2}/>
          </SwiperSlide>
        </Swiper>
      </div>
      <Footer />
    </main>
  );
};
