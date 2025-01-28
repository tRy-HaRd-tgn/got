import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector, X } from "../../imgs";
import { ModalIcon } from "../../components";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { API_URL2 } from "../../http";
import SkinService from "../../services/SkinService";
export const Profile = (props) => {
  const dispatch = useDispatch();
  const [modal, setModal] = useState(false);
  const nickname = useSelector((state) => state.user.nickname);
  const email = useSelector((state) => state.user.email);
  const donate = useSelector((state) => state.user.donate);
  const regDate = useSelector((state) => state.user.regDate);
  const [tempPhoto, setTempPhoto] = useState("");
  const setProfilePhoto = (temp) => {
    dispatch({ type: "SET_PROFILE_PHOTO", profilePhoto: temp });
  };
  const setSkin = (temp) => {
    dispatch({ type: "SET_SKIN", skin: temp });
  };
  const skin = useSelector((state) => state.user.skin); // сохраняем скин в переменную

  useEffect( () => {
    const responce2 =  SkinService.getAvatar();
    setProfilePhoto(API_URL2 + responce2.data);
    console.log(responce2.data);
    const responce3 =  SkinService.getSkin();
    setSkin(API_URL2 + responce3.data);
    console.log(responce3.data);
  }, [tempPhoto]);
  const clickHandler = async (e) => {
    const file = e.target.files[0]; // схватили выбранный файл
    try {
      setTempPhoto(file); // сохраняем в temp загруженное фото
      console.log(file);
      const responce = await SkinService.uploadSkin(tempPhoto); // загружаем скин на бэк
      console.log(responce);
    } catch (e) {
      console.log(e);
    }
  };
  return (
    <main className={styles.main}>
      <ModalIcon active={modal} setState={setModal}>
        <div
          style={{
            marginTop: "5%",
            display: "flex",
            justifyContent: "space-between",
            width: "90%",
          }}
        >
          <h2 className={styles.modalHeader}>Пополнение баланса</h2>
          <img
            style={{ cursor: "pointer" }}
            onClick={() => setModal(false)}
            src={X}
            alt="error"
          />
        </div>
        <input type="number" placeholder="Сумма" className={styles.input} />
        <input
          type="text"
          placeholder="Промокод (если есть)"
          className={styles.input}
        />
        <button
          style={{
            marginBottom: "7%",
            cursor: "pointer",
          }}
          className={styles.button}
        >
          Пополнить
        </button>
      </ModalIcon>
      <Header />
      <div className={styles.description}>
        <h1 style={{ fontSize: "70px" }}>Личный кабинет</h1>
        <div className={styles.menu}>
          <div className={styles.menuSkin}>
            <img className={styles.menuSkinImg} src={skin} alt="error" />
          </div>
          <div className={styles.menuRight}>
            <div className={styles.menuRightTop}>
              <div className={styles.menuRightTopWrapper}>
                <div>
                  <h2 className={styles.menuRightTopH2}>ИНФОРМАЦИЯ</h2>
                  <div className={styles.delimeter}></div>
                </div>
                <p className={styles.menuRightTopWrapperP}>
                  Ваш ник:{" "}
                  <span style={{ color: "white" }}>{" " + nickname}</span>
                </p>
                <p className={styles.menuRightTopWrapperP}>
                  Дата регистрации:{" "}
                  <span style={{ color: "white" }}>{" " + regDate}</span>
                </p>
                <p className={styles.menuRightTopWrapperP}>
                  Ваша почта:{" "}
                  <span style={{ color: "white" }}>{" " + email}</span>
                </p>
                <p className={styles.menuRightTopWrapperP}>
                  Ваш баланс:{" "}
                  <span style={{ color: "white" }}>{" " + donate}</span>{" "}
                  <span style={{ color: "white" }}>Золотых</span>{" "}
                </p>
              </div>
            </div>
            <div className={styles.menuRightBottom}>
              <input
                id="input_file"
                type="file"
                className={styles.menuRightBottomButton}
                style={{ display: "none" }}
                onChange={clickHandler}
              />
              <label className={styles.inputLabel} htmlFor="input_file">
                Сменить скин
              </label>
              <button
                className={styles.menuRightBottomButton}
                onClick={() => {
                  setModal(true);
                }}
              >
                Пополнить баланс
              </button>
            </div>
          </div>
        </div>
      </div>
      <img src={vector} alt="" className={styles.devider} />
      <Footer />
    </main>
  );
};
