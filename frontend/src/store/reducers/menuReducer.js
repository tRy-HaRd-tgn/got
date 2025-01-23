const defaultState = {
  choise: "",
  color: "",
  image: "",
  name: "",
  description: "",
  price: "",
};

export const menuReducer = (state = defaultState, action) => {
  switch (action.type) {
    case "SET_CHOISE":
      return {
        ...state,
        choise: action.choise,
      };
    case "SET_COLOR":
      return {
        ...state,
        color: action.color,
      };
    case "SET_IMAGE":
      return {
        ...state,
        image: action.image,
      };
    default:
      return state;
  }
};
