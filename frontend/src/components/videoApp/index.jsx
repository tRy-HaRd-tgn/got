import React from "react";
import { Video } from "@triyanox/react-video";
import styles from "./styles.module.scss";

// Import custom icons (assuming these are available in your project)
import {
  CustomPlayIcon,
  CustomPauseIcon,
  CustomForwardIcon,
  CustomBackwardIcon,
  CustomEnterPipIcon,
  CustomExitPipIcon,
  CustomVolumeIcon,
  CustomFullScreenIcon,
  CustomExitFullScreenIcon,
  CustomLoadingIcon,
} from "./YourIconPath";

const MyVideoComponent = () => {
  const videoProps = {
    src: [
      {
        src: "https://example.com/video-sd.mp4",
        type: "video/mp4",
        label: "SD",
      },
      {
        src: "https://example.com/video-hd.mp4",
        type: "video/mp4",
        label: "HD",
      },
    ],
    poster: "https://example.com/poster.jpg",
    title: "My Amazing Video",
    subtitle: "An insightful subtitle",
    onProgress: (currentTime) => console.log(`Current Time: ${currentTime}`),
    onDuration: (duration) => console.log(`Duration: ${duration}`),
    onEnded: () => console.log("Video Ended"),
    onPlay: () => console.log("Video Played"),
    onPause: () => console.log("Video Paused"),
    onLoad: () => console.log("Video Loaded"),
    onVolumeChange: (volume) => console.log(`Volume: ${volume}`),
    onPlaybackRateChange: (rate) => console.log(`Playback Rate: ${rate}`),
    className: "custom-video-class",
    autoPlay: true,
    loop: true,
    showControls: true,
    icons: {
      play: CustomPlayIcon,
      pause: CustomPauseIcon,
      forwardBy10: CustomForwardIcon,
      backBy10: CustomBackwardIcon,
      enterPip: CustomEnterPipIcon,
      exitPip: CustomExitPipIcon,
      volume: CustomVolumeIcon,
      fullScreen: CustomFullScreenIcon,
      exitFullScreen: CustomExitFullScreenIcon,
      loading: CustomLoadingIcon,
    },
    classNames: {
      base: "video-base-class",
      title: "video-title-class",
      subtitle: "video-subtitle-class",
      topWrapper: "top-wrapper-class",
      centerWrapper: "center-wrapper-class",
      bottomWrapper: "bottom-wrapper-class",
      video: "video-element-class",
      backdrop: "video-backdrop-class",
      volumeSlider: {
        root: "volume-slider-root-class",
        track: "volume-slider-track-class",
        thumb: "volume-slider-thumb-class",
        range: "volume-slider-range-class",
      },
      playbackRateSlider: {
        root: "playback-rate-slider-root-class",
        track: "playback-rate-slider-track-class",
        thumb: "playback-rate-slider-thumb-class",
        range: "playback-rate-slider-range-class",
      },
    },
    hideSliderThumb: false,
  };

  return <Video {...videoProps} />;
};

export default MyVideoComponent;
