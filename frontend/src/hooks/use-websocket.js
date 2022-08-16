import { useRef, useReducer } from "react";
import { useNavigate } from "react-router-dom";

const useWebsocket = (
  url,
  onOpenHandler,
  onCloseHandler,
  reducer,
  initialState,
  backPathName
) => {
  const navigate = useNavigate();

  const [state, dispatch] = useReducer(reducer, initialState);

  const ws = useRef(null);

  const initializeWebSocket = () => {
    ws.current = new WebSocket(url);
    ws.current.onopen = () => onOpenHandler();
    ws.current.onclose = () => onCloseHandler();
    ws.current.onmessage = (e) => {
      const message = JSON.parse(e.data);
      if (message) {
        dispatch({
          type: message.type.toUpperCase(),
          payload: message.content,
        });
      }
    };
  };

  const closeSessionHandler = () => {
    ws.current.close();
    navigate({ pathname: backPathName }, { replace: true });
  };

  return {
    ws,
    state,
    dispatch,
    initializeWebSocket,
    closeSessionHandler,
  };
};

const gameInitialState = {
  isLoading: false,
  error: null,
  currentProblem: null,
  problemsCounter: 0,
  winner: null,
};

const gameReducer = (state, action) => {
  switch (action.type) {
    case "STARTING":
      return {
        ...state,
        isLoading: false,
      };
    case "ENDING":
      return { ...state, isLoading: false, winner: action.payload };
    case "PROBLEM":
      return {
        ...state,
        isLoading: false,
        currentProblem: { ...action.payload },
        problemsCounter: state.problemsCounter + 1,
      };
    case "ERROR":
      return {
        ...state,
        error: action.payload,
      };
    default: // i.e. "WAITING" and "LOADING"
      return { ...state, isLoading: action.payload || true };
  }
};

const useGameWebSocket = (url, onOpenHandler, onCloseHandler, backPathName) => {
  const { ws, state, dispatch, initializeWebSocket, closeSessionHandler } =
    useWebsocket(
      url,
      onOpenHandler,
      onCloseHandler,
      gameReducer,
      gameInitialState,
      backPathName
    );

  const submitUserAnswerHandler = (payload) => {
    dispatch({ type: "WAITING" });
    ws.current.send(JSON.stringify({ data: payload, action: "user_answer" }));
  };

  return {
    ws,
    state,
    dispatch,
    initializeWebSocket,
    submitUserAnswerHandler,
    closeSessionHandler,
  };
};

export { useGameWebSocket };

export default useWebsocket;
