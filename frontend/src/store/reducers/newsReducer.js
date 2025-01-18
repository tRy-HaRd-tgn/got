const defaultState = {
  news: [],
};

export const newsReducer = (state = defaultState, action) => {
  switch (action.type) {
    case "SET_NEWS":
      return {
        ...state,
        news: action.news,
      };
    default:
      return state;
  }
};

export default newsReducer;