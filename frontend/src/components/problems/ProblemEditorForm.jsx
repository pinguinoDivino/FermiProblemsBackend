import { maxLengthValidation, isBlankValidation } from "../../hooks/use-input";
import useInput from "../../hooks/use-input";
import BaseButton from "../UI/BaseButton/BaseButton";
import BaseUploadFile from "../UI/BaseUploadFile/BaseUploadFile";
import { useState } from "react";

const ProblemEditorForm = (props) => {
  const {
    enteredValue: enteredQuestion,
    valueIsValid: enteredQuestionIsValid,
    hasError: inputQuestionHasError,
    setIsTouched: setInputQuestionIsTouched,
    valueChangeHandler: questionChangeHandler,
    inputBlurHandler: questionBlurHandler,
    reset: resetQuestionInput,
  } = useInput((value) => {
    return isBlankValidation(value) && maxLengthValidation(value, 3000);
  });
  const {
    enteredValue: enteredAnswerValue,
    valueIsValid: enteredAnswerValueIsValid,
    hasError: inputAnswerValueHasError,
    setIsTouched: setInputAnswerValueIsTouched,
    valueChangeHandler: answerValueChangeHandler,
    inputBlurHandler: answerValueBlurHandler,
    reset: resetAnswerValueInput,
  } = useInput((value) => {
    return isBlankValidation(value);
  });
  const {
    enteredValue: enteredAnswer,
    valueIsValid: enteredAnswerIsValid,
    hasError: inputAnswerHasError,
    setIsTouched: setInputAnswerIsTouched,
    valueChangeHandler: answerChangeHandler,
    inputBlurHandler: answerBlurHandler,
    reset: resetAnswerInput,
  } = useInput((value) => {
    return isBlankValidation(value) && maxLengthValidation(value, 3000);
  });

  const {
    enteredValue: enteredExplanation,
    valueIsValid: enteredExplanationIsValid,
    hasError: inputExplanationHasError,
    setIsTouched: setInputExplanationIsTouched,
    valueChangeHandler: explanationChangeHandler,
    inputBlurHandler: explanationBlurHandler,
    reset: resetExplanationInput,
  } = useInput((value) => {
    return maxLengthValidation(value, 10000);
  });

  const [questionImage, setQuestionImage] = useState(null);
  const [answerImage, setAnswerImage] = useState(null);
  const [explanationImage, setExplanationImage] = useState(null);

  const formIsValid =
    enteredQuestionIsValid &&
    enteredAnswerValueIsValid &&
    enteredAnswerIsValid &&
    enteredExplanationIsValid;

  const qImageChangeHandler = (payload) => {
    setQuestionImage(payload);
  };
  const aImageChangeHandler = (payload) => {
    setAnswerImage(payload);
  };
  const eImageChangeHandler = (payload) => {
    setExplanationImage(payload);
  };

  const onSubmitHandler = (event) => {
    event.preventDefault();
    setInputQuestionIsTouched(true);
    setInputAnswerValueIsTouched(true);
    setInputAnswerIsTouched(true);
    setInputExplanationIsTouched(true);
    if (!formIsValid) {
      return;
    }
    const obj = {
      question: enteredQuestion,
      value: +enteredAnswerValue,
      answer: enteredAnswer,
      explanation: enteredExplanation,
    };
    const json = JSON.stringify(obj);
    const blob = new Blob([json], {
      type: "application/json",
    });
    const data = new FormData();
    data.append("document", blob);
    questionImage && data.append("q_image", questionImage, questionImage.name);
    answerImage && data.append("a_image", answerImage, answerImage.name);
    explanationImage &&
      data.append("e_image", explanationImage, explanationImage.name);

    props.onSubmitForm(data);
    resetQuestionInput();
    resetAnswerValueInput();
    resetAnswerInput();
    resetExplanationInput();
  };

  const backHandler = () => {
    props.onBack();
  };

  const inputQuestionClasses = inputQuestionHasError
    ? "form-control invalid"
    : "form-control";

  const inputAnswerValueClasses = inputAnswerValueHasError
    ? "form-control invalid"
    : "form-control";

  const inputAnswerClasses = inputAnswerHasError
    ? "form-control invalid"
    : "form-control";

  const inputExplanationClasses = inputExplanationHasError
    ? "form-control invalid"
    : "form-control";

  return (
    <form onSubmit={onSubmitHandler}>
      <div className={inputQuestionClasses}>
        <label htmlFor="enteredQuestion">
          <strong>Domanda</strong>
        </label>
        <input
          id="enteredQuestion"
          type="text"
          onChange={questionChangeHandler}
          value={enteredQuestion}
          onBlur={questionBlurHandler}
        />
        {inputQuestionHasError && (
          <div className="invalid-message">
            Non può essere nullo e deve essere minore di 3000 caratteri!
          </div>
        )}
      </div>
      <div className={inputAnswerValueClasses}>
        <label htmlFor="enteredAnswerValue">
          <strong>Valore risposta</strong>
        </label>
        <input
          id="enteredAnswerValue"
          type="number"
          onChange={answerValueChangeHandler}
          value={enteredAnswerValue}
          onBlur={answerValueBlurHandler}
        />
        {inputAnswerValueHasError && (
          <div className="invalid-message">Non può essere nullo!</div>
        )}
      </div>
      <div className={inputAnswerClasses}>
        <label htmlFor="enteredAnswer">
          <strong>Testo della risposta</strong>
        </label>
        <input
          id="enteredAnswer"
          type="text"
          onChange={answerChangeHandler}
          value={enteredAnswer}
          onBlur={answerBlurHandler}
        />
        {inputAnswerHasError && (
          <div className="invalid-message">
            Non può essere nullo e deve essere minore di 3000 caratteri!
          </div>
        )}
      </div>
      <div className={inputExplanationClasses}>
        <label htmlFor="enteredExplanation">
          <strong>Spiegazione</strong>
        </label>
        <textarea
          id="enteredExplanation"
          cols="8"
          rows="7"
          onChange={explanationChangeHandler}
          value={enteredExplanation}
          onBlur={explanationBlurHandler}
        />
        {inputExplanationHasError && (
          <div className="invalid-message">
            Deve essere minore di 10.000 caratteri!
          </div>
        )}
      </div>
      <div className="form-control row">
        <div className="col-lg-4">
          <label>Immagine domanda</label>
          <BaseUploadFile
            name="question-upload"
            onFileChange={qImageChangeHandler}
          />
        </div>
        <div className="col-lg-4">
          <label>Immagine risposta</label>
          <BaseUploadFile
            name="answer-upload"
            onFileChange={aImageChangeHandler}
          />
        </div>
        <div className="col-lg-4">
          <label>Immagine spiegazione</label>
          <BaseUploadFile
            name="explanation-upload"
            onFileChange={eImageChangeHandler}
          />
        </div>
      </div>
      <div className="form-control mt-1">
        <BaseButton type="submit" mode="success">
          Invia
        </BaseButton>
        <BaseButton type="button" mode="danger" onClick={backHandler}>
          Indietro
        </BaseButton>
      </div>
    </form>
  );
};

export default ProblemEditorForm;
