import styles from "./styles.module.scss";
import ReactSkinview3d from "react-skinview3d";
import { Header, Footer, ModalIcon } from "../../components";
import { vector, X } from "../../imgs";
import { useEffect, useState, React } from "react";
import { useDispatch, useSelector } from "react-redux";
import { API_URL2 } from "../../http";
import SkinService from "../../services/SkinService";
import PaymentService from "../../services/PamentService";
export const Profile = () => {
  const dispatch = useDispatch();
  const [modal, setModal] = useState(false);
  const nickname = useSelector((state) => state.user.nickname);
  const email = useSelector((state) => state.user.email);
  const donate = useSelector((state) => state.user.donate);
  const regDate = useSelector((state) => state.user.regDate);
  const [promo, setPromo] = useState("");
  const [currency, setCurrency] = useState("");

  const setProfilePhoto = (temp) => {
    dispatch({ type: "SET_PROFILE_PHOTO", profilePhoto: temp });
  };
  const setSkin = (temp) => {
    dispatch({ type: "SET_SKIN", skin: temp });
  };
  const skin = useSelector((state) => state.user.skin);
  const configureStore = async () => {
    const responce2 = await SkinService.getAvatar();
    setProfilePhoto(API_URL2 + "/" + responce2.data);
    const responce3 = await SkinService.getSkin();
    setSkin(API_URL2 + "/" + responce3.data);
  };
  useEffect(() => {
    configureStore();
  }, []);
  const clickHandler = (e) => {
    const file = e.target.files[0];
    try {
      const formData = new FormData();
      formData.append("skin", file);
      SkinService.uploadSkin(formData);
      window.location.reload();
    } catch (e) {
      console.log(e);
    }
  };
  async function buyDonate() {
    console.log("buy donate");
    try {
      const responce = await PaymentService.addBalance(Number(currency));
      window.location.replace(responce.data.payment_url)
      console.log(responce);
    } catch (e) {
      console.error(e);
    }
  }
  return (
    <main className={styles.main}>
      <ModalIcon active={modal} setState={setModal}>
        <div
          style={{
            marginTop: "5%",
            display: "flex",
            justifyContent: "space-between",
            width: "90%",
            height: "10%",
          }}
        >
          <h2 className={styles.modalHeader}>Пополнение баланса</h2>
          <img
            style={{ cursor: "pointer", height: "30%" }}
            onClick={() => setModal(false)}
            src={X}
            alt="error"
          />
        </div>
        <input
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          type="number"
          placeholder="Сумма"
          className={styles.input}
        />
        <input
          type="text"
          placeholder="Промокод (если есть)"
          className={styles.input}
          value={promo}
          onChange={(e) => setPromo(e.target.value)}
        />
        <button
          style={{
            marginBottom: "7%",
            cursor: "pointer",
          }}
          className={styles.button}
          onClick={() => {
            buyDonate();
          }}
        >
          Пополнить
        </button>
      </ModalIcon>
      <Header />
      <div className={styles.description}>
        <h1 style={{ fontSize: "70px" }}>Личный кабинет</h1>
        <div className={styles.menu}>
          <div className={styles.menuSkin}>
            <ReactSkinview3d
              width="500"
              height="500"
              className={styles.skin}
              skinUrl={skin}
            />
          </div>
          <div className={styles.menuRight}>
            <div className={styles.menuRightTop}>
              <div className={styles.menuRightTopWrapper}>
                <div>
                  <h2 className={styles.menuRightTopH2}>ИНФОРМАЦИЯ</h2>
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
              <label
                title="используейте пожалуйста файл 64x64"
                className={styles.inputLabel}
                htmlFor="input_file"
              >
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
