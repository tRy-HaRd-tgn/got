import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector } from "../../imgs";
import { useState } from "react";
import { DonateComp } from "../../components";
import { useEffect } from "react";
import DonationService from "../../services/DonationService";
import { ModalIcon } from "../../components";
import { useSelector } from "react-redux";
export const Donate = (props) => {
  const color = useSelector((state) => state.menu.color);
  const img = useSelector((state) => state.menu.image);
  const [choise, setChoise] = useState("privileges");
  const [priviligies, setPriviligies] = useState([]);
  const [pets, setPets] = useState([]);
  const [mounts, setMounts] = useState([]);
  const [other, setOthers] = useState([]);
  const [modal, setModal] = useState(false);
  const [rr, setRr] = useState(false);
  const [gg, setGg] = useState(false);
  const [bb, setBb] = useState(false);
  const [image, setImage] = useState(null);
  useEffect(() => {
    try {
      const responce = DonationService.getDonations();
      responce.then((value) => {
        console.log(value.data);
        let newPrivileges = [];
        let newPets = [];
        let newMounts = [];
        let newOther = [];
        for (let i = 0; i < value.data.length; i++) {
          if (value.data[i].category == "privileges") {
            newPrivileges.push(value.data[i]);
          }
          if (value.data[i].category == "pets") {
            newPets.push(value.data[i]);
          }
          if (value.data[i].category == "mounts") {
            newMounts.push(value.data[i]);
          }
          if (value.data[i].category == "other") {
            newOther.push(value.data[i]);
          }
        }
        setPriviligies(newPrivileges);
        setPets(newPets);
        setMounts(newMounts);
        setOthers(newOther);
      });
    } catch (e) {
      console.log(e?.responce?.data?.message);
    }
  }, []);
  console.log(priviligies);
  const func = (state) => {
    switch (state) {
      case "privileges": {
        return priviligies.map((value, index) => (
          <DonateComp
            setModal={setModal}
            text={value.name}
            price={value.price}
            img={value.image_url}
            key={index}
            color={value.background_color}
          />
        ));
      }
      case "pets": {
        return pets.map((value, index) => (
          <DonateComp
            setModal={setModal}
            text={value.name}
            price={value.price}
            img={value.image_url}
            key={index}
            color={value.background_color}
          />
        ));
      }
      case "mounts": {
        return mounts.map((value, index) => (
          <DonateComp
            setModal={setModal}
            text={value.name}
            price={value.price}
            img={value.image_url}
            key={index}
            color={value.background_color}
          />
        ));
      }
      case "other": {
        return other.map((value, index) => (
          <DonateComp
            setModal={setModal}
            text={value.name}
            price={value.price}
            img={value.image_url}
            key={index}
            color={value.background_color}
          />
        ));
      }
    }
  };
  const checkBackground = (choise) => {
    switch (choise) {
      case "privileges": {
        return `url('src/imgs/backgrounds/prev.png')`;
      }
      case "pets": {
        return `url('src/imgs/backgrounds/donate.png')`;
      }
      case "mounts": {
        return `url('src/imgs/backgrounds/mounts.png')`;
      }
      case "other": {
        return `url('src/imgs/backgrounds/other.png')`;
      }
    }
  };
  return (
    <>
      <ModalIcon style={{ width: "100vw" }} active={modal} setState={setModal}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            width: "100%",
            height: "100%",
          }}
        >
          <div className={styles.imgWrapper}>
            <img style={{ width: "100%", height: "100%" }} src={img} alt="" />
          </div>
          <p>2</p>
          <p>3</p>
        </div>
      </ModalIcon>
      <main className={styles.main}>
        <Header />
        <div
          style={{ backgroundImage: checkBackground(choise) }}
          className={styles.description}
        >
          <h1 className={styles.h1}>донат магазин</h1>
          <div className={styles.descriptionDiv}>
            <button
              className={styles.descriptionDivButton}
              style={
                choise == "privileges" ? { backgroundColor: "#181f37" } : {}
              }
              onClick={() => setChoise("privileges")}
            >
              Привилегии
            </button>
            <button
              className={styles.descriptionDivButton}
              style={choise == "pets" ? { backgroundColor: "#181f37" } : {}}
              onClick={() => setChoise("pets")}
            >
              питомцы
            </button>
            <button
              className={styles.descriptionDivButton}
              style={choise == "mounts" ? { backgroundColor: "#181f37" } : {}}
              onClick={() => setChoise("mounts")}
            >
              маунты
            </button>
            <button
              className={styles.descriptionDivButton}
              style={choise == "other" ? { backgroundColor: "#181f37" } : {}}
              onClick={() => setChoise("other")}
            >
              разное
            </button>
          </div>
          <div className={styles.donateWrapper}>{func(choise)}</div>
        </div>
        <img src={vector} alt="" className={styles.devider} />
        <div className={styles.project}></div>
        <Footer />
      </main>
    </>
  );
};
