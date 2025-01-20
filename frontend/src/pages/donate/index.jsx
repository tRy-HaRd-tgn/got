import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector } from "../../imgs";
import { useState } from "react";
import { DonateComp } from "../../components";
import { useEffect } from "react";
import DonationService from "../../services/DonationService";
export const Donate = (props) => {
  const [choise, setChoise] = useState("");
  const [priviligies, setPriviligies] = useState([]);
  const [pets, setPets] = useState([]);
  const [mounts, setMounts] = useState([]);
  const [other, setOthers] = useState([]);
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
          <DonateComp text={value.name} price={value.price} key={index} />
        ));
      }
      case "pets": {
        return pets.map((value, index) => (
          <DonateComp text={value.name} price={value.price} key={index} />
        ));
      }
      case "mounts": {
        return mounts.map((value, index) => (
          <DonateComp text={value.name} price={value.price} key={index} />
        ));
      }
      case "other": {
        return other.map((value, index) => (
          <DonateComp text={value.name} price={value.price} key={index} />
        ));
      }
    }
  };
  return (
    <main className={styles.main}>
      <Header />
      <div className={styles.description}>
        <h1 className={styles.h1}>донат магазин</h1>
        <div className={styles.descriptionDiv}>
          <button
            className={styles.descriptionDivButton}
            style={choise == "privileges" ? { backgroundColor: "green" } : {}}
            onClick={() => setChoise("privileges")}
          >
            Привилегии
          </button>
          <button
            className={styles.descriptionDivButton}
            style={choise == "pets" ? { backgroundColor: "green" } : {}}
            onClick={() => setChoise("pets")}
          >
            питомцы
          </button>
          <button
            className={styles.descriptionDivButton}
            style={choise == "mounts" ? { backgroundColor: "green" } : {}}
            onClick={() => setChoise("mounts")}
          >
            маунты
          </button>
          <button
            className={styles.descriptionDivButton}
            style={choise == "other" ? { backgroundColor: "green" } : {}}
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
  );
};
