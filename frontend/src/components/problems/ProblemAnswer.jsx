import { useState } from "react";
import ProblemExplanation from "./ProblemExplanation";
import ProblemDistribution from "./ProblemDistribution";
import BaseButton from "../UI/BaseButton/BaseButton";
import BaseModal from "../UI/BaseModal/BaseModal";

const ProblemAnswer = (props) => {
  const [showExplanation, setShowExplanation] = useState(false);

  const [showDistribution, setShowDistribution] = useState(false);

  const toggleExplanationSection = () => {
    setShowExplanation((prevState) => {
      return !prevState;
    });
  };

  const toggleDistributionSection = () => {
    setShowDistribution((prevState) => {
      return !prevState;
    });
  };

  const onClickNextProblemHandler = () => {
    setShowExplanation(false);
    setShowDistribution(false);
    props.onNextQuestion();
  };

  return (
    <div className={props.className}>
      <h2>Soluzione:</h2>
      <h3>{props.problem.value}</h3>
      <p>{props.problem.answer}</p>

      {showExplanation && (
        <ProblemExplanation
          explanation={props.problem.explanation}
          image={props.problem.e_image}
          onClose={toggleExplanationSection}
        />
      )}
      {showDistribution && (
        <BaseModal onClose={toggleDistributionSection}>
          <ProblemDistribution onClose={toggleDistributionSection} />
        </BaseModal>
      )}
      <hr />
      <BaseButton
        onClick={onClickNextProblemHandler}
        type="button"
        mode="success"
      >
        Prossima domanda
      </BaseButton>
      {!showExplanation && (
        <BaseButton
          type="button"
          onClick={toggleExplanationSection}
          mode="info"
        >
          Mostra spiegazione
        </BaseButton>
      )}
      {!showDistribution && (
        <BaseButton
          type="button"
          onClick={toggleDistributionSection}
          mode="outline"
        >
          Mostra le risposte degli altri utenti
        </BaseButton>
      )}
    </div>
  );
};

export default ProblemAnswer;
