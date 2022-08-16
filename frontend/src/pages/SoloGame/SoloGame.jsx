import { useEffect } from "react";
import ProblemQuestion from "../../components/problems/ProblemQuestion";
import ProblemAnswer from "../../components/problems/ProblemAnswer";
import { useGameWebSocket } from "../../hooks/use-websocket";
import classes from "./SoloGame.module.css";

const SoloGame = () => {
  const {
    ws,
    state,
    dispatch,
    initializeWebSocket,
    submitUserAnswerHandler,
    closeSessionHandler,
  } = useGameWebSocket(
    `ws://${window.location.host}/ws/games/solo/`,
    () => console.log("ws opened"),
    () => console.log("ws closed"),
    "/allenamento"
  );

  useEffect(() => {
    initializeWebSocket();
    const wsCurrent = ws.current;
    return () => {
      wsCurrent.close();
    };
  }, []);

  const nextProblemHandler = () => {
    dispatch({ type: "NEXT", payload: false });
    ws.current.send(JSON.stringify({ action: "next_problem" }));
  };
  const {
    isLoading: showAnswer,
    error,
    currentProblem,
    problemsCounter,
  } = state;
  const showProblemSection = currentProblem && !showAnswer;

  return (
    <div className={classes.container}>
      <h1>Problema n. {problemsCounter}</h1>
      {showProblemSection && (
        <ProblemQuestion
          problem={currentProblem}
          onSubmitUserAnswer={submitUserAnswerHandler}
          onCloseSession={closeSessionHandler}
        />
      )}
      {showAnswer && (
        <ProblemAnswer
          problem={currentProblem}
          onNextQuestion={nextProblemHandler}
        />
      )}
      {error && (
        <div className="invalid-message">
          <p>{error}</p>{" "}
        </div>
      )}
    </div>
  );
};

export default SoloGame;
