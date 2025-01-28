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
  useEffect(() => {
    try {
      const responce = DonationService.getDonations();
      responce.then((value) => {
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

  const func1 = (choise) => {
    console.log(priviligies);
    if (choise == "privileges") {
      return priviligies.map((value, index) => (
        <DonateComp
          id={value.id}
          text={value.name}
          price={value.price}
          img={value.image_url}
          key={index}
          description={value.description}
          color={value.background_color}
        />
      ));
    }
  };

  const func2 = (choise) => {
    if (choise == "pets") {
      console.log(pets);
      return pets.map((value, index) => (
        <DonateComp
          id={value.id}
          text={value.name}
          price={value.price}
          img={value.image_url}
          key={index}
          description={value.description}
          color={value.background_color}
        />
      ));
    }
  };
  const func3 = (choise) => {
    console.log(mounts);
    if (choise == "mounts") {
      return mounts.map((value, index) => (
        <DonateComp
          id={value.id}
          text={value.name}
          price={value.price}
          img={value.image_url}
          key={index}
          description={value.description}
          color={value.background_color}
        />
      ));
    }
  };
  const func4 = (choise) => {
    console.log(other);
    if (choise == "other") {
      return other.map((value, index) => (
        <DonateComp
          id={value.id}
          text={value.name}
          price={value.price}
          img={value.image_url}
          key={index}
          description={value.description}
          color={value.background_color}
        />
      ));
    }
  };
  const checkBackground = (choise) => {
    switch (choise) {
      case "privileges": {
        return styles.privileges;
      }
      case "pets": {
        return styles.pets;
      }
      case "mounts": {
        return styles.mounts;
      }
      case "other": {
        return styles.other;
      }
    }
  };
  return (
    <>
      <main className={styles.main}>
        <Header />
        <div className={styles.description + " " + checkBackground(choise)}>
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
          {choise == "privileges" ? (
            <div className={styles.donateWrapper}>{func1(choise)}</div>
          ) : null}
          {choise == "pets" ? (
            <div className={styles.donateWrapper}>{func2(choise)}</div>
          ) : null}
          {choise == "mounts" ? (
            <div className={styles.donateWrapper}>{func3(choise)}</div>
          ) : null}
          {choise == "other" ? (
            <div className={styles.donateWrapper}>{func4(choise)}</div>
          ) : null}
        </div>
        <img src={vector} alt="" className={styles.devider} />
        <div className={styles.project}></div>
        <Footer />
      </main>
    </>
  );
};
