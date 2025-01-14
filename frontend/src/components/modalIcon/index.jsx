import styles from "./styles.module.scss";
export const ModalIcon = ({ state, setState, active, children, setActive }) => {
  const swapStates = () => {
    if(setState){
        setState(false);
    }
    if(setActive){
        setActive(false);
    }
  };
  const classnames = () => {
    return active ? !state ?styles.modal__content: styles.modal__content_active : styles.modal__content_active;
  };
  return (
    <>
      <div
        className={active ? styles.modal_active : styles.modal}
        onClick={swapStates}
      >
        <div
          className={classnames()}
          styles={state ? { width: "70vh", height: "150vh" } : {}}
          onClick={(e) => e.stopPropagation()}
        >
          {children}
        </div>
      </div>
    </>
  );
};
