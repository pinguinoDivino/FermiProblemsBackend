import { useState, useEffect } from "react";

import classes from "./BaseTimer.module.css";

const BaseTimer = (props) => {
  const [counter, setCounter] = useState(props.maxTime);

  useEffect(() => {
    const timer =
      counter > 0 && setInterval(() => setCounter(counter - 1), 1000);
    return () => clearInterval(timer);
  }, [counter]);

  useEffect(() => {
    if (counter === 0) {
      props.onTimeOut();
    }
  }, [counter]);

  return <div className={classes.timer}>Countdown: {counter}</div>;
};

export default BaseTimer;
