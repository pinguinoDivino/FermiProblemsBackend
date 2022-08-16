import BaseButton from "../UI/BaseButton/BaseButton";
import useInput from "../../hooks/use-input";
import classes from "./ProblemQuestion.module.css";

const ProblemQuestion = (props) => {
  const {
    enteredValue: inputValue,
    valueIsValid,
    setIsTouched,
    valueChangeHandler,
    inputBlurHandler,
    reset,
    hasError,
  } = useInput((value) => value.trim() !== "");

  const onSubmitHandler = (event) => {
    event.preventDefault();
    setIsTouched(true);
    if (!valueIsValid) {
      return;
    }
    props.onSubmitUserAnswer({
      value: +inputValue,
    });

    reset();
  };

  const closeSessionHandler = () => {
    props.onCloseSession();
  };

  const inputClasses = hasError ? "form-control invalid" : "form-control";

  return (
    <div className={props.className}>
      <h2>{props.problem.question}</h2>
      {props.problem.q_image && (
        <div className={classes["img-container"]}>
          <img
            className={classes["img-responsive"]}
            src={props.problem.q_image}
            alt="problem img"
          />
        </div>
      )}
      <form onSubmit={onSubmitHandler} className={classes.form}>
        <div className={inputClasses}>
          <label htmlFor="inputValue">
            <strong>La tua risposta</strong>
          </label>
          <input
            id="inputValue"
            type="number"
            onChange={valueChangeHandler}
            value={inputValue}
            onBlur={inputBlurHandler}
          />
          {hasError && (
            <div className="invalid-message">Non può essere nullo</div>
          )}
        </div>
        <BaseButton type="submit" mode="outline">
          Invia
        </BaseButton>
        <BaseButton type="button" mode="danger" onClick={closeSessionHandler}>
          Indietro
        </BaseButton>
      </form>
    </div>
  );
};

export default ProblemQuestion;
