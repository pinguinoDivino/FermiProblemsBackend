import BaseButton from "../UI/BaseButton/BaseButton";

const ProblemExplanation = (props) => {
  const onClickCloseHandler = () => {
    props.onClose();
  };
  return (
    <div>
      <h1>Spiegazione</h1>
      <p>{props.explanation}</p>
      <BaseButton
        mode="danger"
        type="button"
        onClick={onClickCloseHandler}
        size="small"
      >
        Chiudi
      </BaseButton>
    </div>
  );
};

export default ProblemExplanation;
