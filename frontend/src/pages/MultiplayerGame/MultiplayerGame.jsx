import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import BaseSpinner from "../../components/UI/BaseSpinner/BaseSpinner";
import ProblemQuestion from "../../components/problems/ProblemQuestion";
import BaseTimer from "../../components/UI/BaseTimer/BaseTimer";

import { useGameWebSocket } from "../../hooks/use-websocket";

import classes from "./MultiplayerGame.module.css";

const maxTime = 10;

const MultiplayerGame = () => {
  const location = useLocation();
  const {
    ws,
    state,
    dispatch,
    initializeWebSocket,
    submitUserAnswerHandler,
    closeSessionHandler,
  } = useGameWebSocket(
    `ws://${window.location.host}/ws/games/multiplayer/${+location.state
      .gameID}/`,
    () => console.log("ws opened"),
    () => console.log("ws closed"),
    "/sfida"
  );

  useEffect(() => {
    initializeWebSocket();
    const wsCurrent = ws.current;
    return () => {
      wsCurrent.close();
    };
  }, []);

  const timeOutHandler = () => {
    dispatch({ type: "LOADING" });
    ws.current.send(JSON.stringify({ action: "time_out" }));
  };
  const { isLoading, error, currentProblem, problemsCounter, winner } = state;
  const showProblemSection = currentProblem && !isLoading && !winner;

  return (
    <div className={classes.container}>
      <h1>SFIDAA SESSIONE n. {problemsCounter}</h1>
      {isLoading && (
        <div>
          <BaseSpinner> </BaseSpinner>
          <p>
            <i>in attesa dello sfidante</i>
          </p>
        </div>
      )}
      {showProblemSection && (
        <>
          <BaseTimer maxTime={maxTime} onTimeOut={timeOutHandler} />
          <ProblemQuestion
            problem={currentProblem}
            onSubmitUserAnswer={submitUserAnswerHandler}
            onCloseSession={closeSessionHandler}
          />
        </>
      )}

      {!!winner && (
        <div>
          <p>Il vincitore è {winner}</p>
        </div>
      )}

      {error && (
        <div className="invalid-message">
          <p>{error}</p>{" "}
        </div>
      )}
    </div>
  );
};

export default MultiplayerGame;
