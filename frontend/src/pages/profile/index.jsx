import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector, X } from "../../imgs";
import { ModalIcon } from "../../components";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
export const Profile = (props) => {
  const dispath = useDispatch();
  const [modal, setModal] = useState(false);
  const nickname = useSelector((state) => state.user.nickname);
  const email = useSelector((state) => state.user.email);
  const donate = useSelector((state) => state.user.donate);
  const regDate = useSelector((state) => state.user.regDate);
  const setPhoto = (skin) => {
    dispath({ type: "SET_SKIN", skin: skin });
  };

  const clickHandler = (e) => {
    const file = e.target.files[0]; // схватили выбранный файл
    console.log(file);
    if (file) {
      setPhoto(URL.createObjectURL(file));
      const skin = useSelector((state) => state.user.skin);
    }
  };
  const skin = useSelector((state) => state.user.skin);
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
        <input
          type="number"
          placeholder="Сумма"
          className={styles.button}
        ></input>
        <input
          type="text"
          placeholder="Промокод (если есть)"
          className={styles.button}
        ></input>
        <button
          style={{
            marginBottom: "7%",
            background: "#181F37",
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
