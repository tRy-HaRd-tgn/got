import { SwiperSlide } from "swiper/react";
import "swiper/css";
export const Video = ({ value }) => {
  return (
    <SwiperSlide>
      <iframe
        width="100%"
        height="100%"
        src={value.url}
        title={value.title}
        frameBorder="0"
        allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerPolicy="strict-origin-when-cross-origin"
        allowFullScreen
      />
    </SwiperSlide>
  );
};