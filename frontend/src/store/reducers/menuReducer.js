const defaultState = {
  choise: "",
};

export const menuReducer = (state = defaultState, action) => {
  switch (action.type) {
    case "SET_CHOISE":
      return {
        ...state,
        choise: action.choise,
      };
    default:
      return state;
  }
};
