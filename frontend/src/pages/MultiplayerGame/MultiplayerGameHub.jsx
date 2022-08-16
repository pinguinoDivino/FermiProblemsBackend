import BaseButton from "../../components/UI/BaseButton/BaseButton";
import { axiosService, catchAxiosError } from "../../common/api.service";
import { useState } from "react";

import { useNavigate } from "react-router-dom";

import classes from "./MultiplayerGameHub.module.css";

const MultiplayerGameHub = () => {
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const searchGameHandler = async () => {
    try {
      const response = await axiosService("/api/games/multiplayer/start/");
      const responseData = await response.data;
      setError(null);
      navigate(
        { pathname: "/sfida/sessione" },
        { state: { gameID: responseData.id } }
      );
    } catch (e) {
      const error = catchAxiosError(
        e,
        "Errore durante la configurazione del gioco"
      );
      setError(error.message);
    }
  };

  return (
    <div className={classes["container-lobby"]}>
      <h1>Sfida un altro giocatore!</h1>
      <div className={classes["lobby"]}>
        <div className={classes["inner-lobby"]}>
          <div>
            <div className={classes.number}>1</div>
            <div className={classes.description}>Once for blood</div>
          </div>
          <div>
            <div className={classes.number}>3</div>
            <div className={classes.description}>Quick Game</div>
          </div>
          <div>
            <div className={classes.number}>5</div>
            <div className={classes.description}>Rapid Game</div>
          </div>
          <div>
            <div className={classes.number}>9</div>
            <div className={classes.description}>Normal Game</div>
          </div>
          <div>
            <div className={classes.number}>11</div>
            <div className={classes.description}>Averaged Game</div>
          </div>
          <div>
            <div className={classes.number}>15</div>
            <div className={classes.description}>Long Game</div>
          </div>
          <div>
            <div className={classes.number}>21</div>
            <div className={classes.description}>IronMan Game</div>
          </div>
          <div>
            <div className={classes.number}>29</div>
            <div className={classes.description}>Hero Game</div>
          </div>
        </div>
      </div>

      <BaseButton mode="outline" onClick={searchGameHandler}>
        Cerca
      </BaseButton>

      {error && <p>{error}</p>}
    </div>
  );
};

export default MultiplayerGameHub;
