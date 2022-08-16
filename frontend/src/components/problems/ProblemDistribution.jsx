import BaseButton from "../UI/BaseButton/BaseButton";

const ProblemDistribution = (props) => {
  const onClickCloseHandler = () => {
    props.onClose();
  };

  return (
    <div>
      <h1>Distribuzione</h1>
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

export default ProblemDistribution;
