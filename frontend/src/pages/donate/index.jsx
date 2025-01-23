import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector } from "../../imgs";
import { useState } from "react";
import { DonateComp } from "../../components";
import { useEffect } from "react";
import DonationService from "../../services/DonationService";

export const Donate = (props) => {
  const [choise, setChoise] = useState("privileges");
  const [priviligies, setPriviligies] = useState([]);
  const [pets, setPets] = useState([]);
  const [mounts, setMounts] = useState([]);
  const [other, setOthers] = useState([]);
  const [temp, setTemp] = useState(0);
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

  const func = (state) => {
    
    switch (state) {
      case "privileges": {
        return priviligies.map((value, index) => (
          <DonateComp
            text={value.name}
            price={value.price}
            img={value.image_url}
            key={index}
            description={value.description}
            color={value.background_color}
          />
        ));
      }
      case "pets": {
        return pets.map((value, index) => (
          <DonateComp
            text={value.name}
            price={value.price}
            img={value.image_url}
            key={index}
            description={value.description}
            color={value.background_color}
          />
        ));
      }
      case "mounts": {
        return mounts.map((value, index) => (
          <DonateComp
            text={value.name}
            price={value.price}
            img={value.image_url}
            key={index}
            description={value.description}
            color={value.background_color}
          />
        ));
      }
      case "other": {
        return other.map((value, index) => (
          <DonateComp
            text={value.name}
            price={value.price}
            img={value.image_url}
            key={index}
            description={value.description}
            color={value.background_color}
          />
        ));
      }
    }
  };
  const checkBackground = (choise) => {
    switch (choise) {
      case "privileges": {
        console.log(priviligies);
        return `url('src/imgs/backgrounds/prev.png')`;
      }
      case "pets": {
        console.log(pets);
        return `url('src/imgs/backgrounds/donate.png')`;
      }
      case "mounts": {
        console.log(mounts);
        return `url('src/imgs/backgrounds/mounts.png')`;
      }
      case "other": {
        console.log(other);
        return `url('src/imgs/backgrounds/other.png')`;
      }
    }
  };
  return (
    <>
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
              onClick={() => {
                setChoise("other");
              }}
            >
              разное
            </button>
          </div>
          <div className={styles.donateWrapper}>{func(choise)}</div>{" "}
        </div>
        <img src={vector} alt="" className={styles.devider} />
        <div className={styles.project}></div>
        <Footer />
      </main>
    </>
  );
};
