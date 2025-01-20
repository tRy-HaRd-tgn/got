const defaultState = {
  email: "undefined",
  password: "undefined",
  nickname: "undefined",
  donate: 0,
  regDate: "undefined",
  skin:'',
  info: {},
};
export const userReducer = (state = defaultState, action) => {
  switch (action.type) {
    case "SET_EMAIL":
      return {
        ...state,
        email: action.email,
      };
    case "SET_PASSWORD":
      return {
        ...state,
        password: action.password,
      };
    case "SET_NICKNAME":
      return {
        ...state,
        nickname: action.nickname,
      };
    case "SET_DONATE":
      return {
        ...state,
        donate: action.donate,
      };
    case "SET_INFO":
      return {
        ...state,
        info: action.info,
      };
    case "SET_REGDATE":
      return {
        ...state,
        regDate: action.regDate,
      };
    case "SET_SKIN":
      return {
        ...state,
        skin: action.skin,
      };
    default:
      return state;
  }
};
