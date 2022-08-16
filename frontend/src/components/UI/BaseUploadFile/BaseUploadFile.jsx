import { useRef, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCloudArrowUp } from "@fortawesome/free-solid-svg-icons";

import classes from "./BaseUploadFile.module.css";

const BaseUploadFile = (props) => {
  const hiddenFileInput = useRef(null);
  const [uploadedFileName, setUploadedFileName] = useState(null);

  const handleChange = (event) => {
    const fileUploaded = event.target.files[0];
    setUploadedFileName(fileUploaded.name);
    props.onFileChange(fileUploaded);
  };
  return (
    <div className={classes["custom-file-upload"]}>
      <span id={props.name} className={classes["file-name"]}>
        {uploadedFileName}
      </span>
      <span className={classes["file-input-container"]}>
        <FontAwesomeIcon
          icon={faCloudArrowUp}
          className={classes["upload-icon"]}
        />
        <input
          id={"file-" + props.name}
          type="file"
          ref={hiddenFileInput}
          onChange={handleChange}
        />
        <label htmlFor={"file-" + props.name}>Seleziona un file</label>
      </span>
    </div>
  );
};

export default BaseUploadFile;
