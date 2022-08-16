import { axiosService, catchAxiosError } from "../../common/api.service";
import { useState } from "react";
import ProblemEditorForm from "../../components/problems/ProblemEditorForm";
import { useNavigate } from "react-router-dom";

const ProblemEditor = () => {
  const navigate = useNavigate();

  const [error, setError] = useState(""); //TODO sistemare html

  const backHandler = () => {
    navigate({ pathname: "/" });
  };

  const submitFormHandler = async (payload) => {
    setError("");
    try {
      const response = await axiosService("/api/problems/", "POST", payload);
      console.log(response);
      navigate({ pathname: "/" });
    } catch (e) {
      const error = catchAxiosError(
        e,
        "Impossibile aggiungere un nuovo problema!"
      );
      setError(error);
    }
  };

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-12">
          <h1>Aggiungi un problema</h1>
        </div>
      </div>
      <div className="row">
        <div className="col-12">
          <ProblemEditorForm
            onBack={backHandler}
            onSubmitForm={submitFormHandler}
          />
          {error && <div>Errore</div>}
        </div>
      </div>
    </div>
  );
};

export default ProblemEditor;
