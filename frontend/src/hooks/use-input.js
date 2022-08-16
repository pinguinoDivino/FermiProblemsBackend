import { useState } from "react";

const isBlankValidation = (value) => {
  return value !== null && value !== undefined && value.trim() !== "";
};

const maxLengthValidation = (value, maxLength) => {
  if (value) {
    return value.length < maxLength;
  }
};

const useInput = (validateValue) => {
  const [enteredValue, setEnteredValue] = useState("");
  const [isTouched, setIsTouched] = useState(false);

  const valueIsValid = validateValue(enteredValue);
  const hasError = !valueIsValid && isTouched;

  const valueChangeHandler = (event) => {
    setEnteredValue(event.target.value);
  };

  const inputBlurHandler = () => {
    setIsTouched(true);
  };

  const reset = () => {
    setEnteredValue("");
    setIsTouched(false);
  };

  return {
    enteredValue,
    valueIsValid,
    hasError,
    setIsTouched,
    valueChangeHandler,
    inputBlurHandler,
    reset,
  };
};

export { maxLengthValidation, isBlankValidation };

export default useInput;
