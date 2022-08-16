import classes from "./BaseSpinner.module.css";

const BaseSpinner = () => {
  return (
    <div className={classes.spinner}>
      <div className={classes["lds-roller"]}>
        <div />
        <div />
        <div />
        <div />
        <div />
        <div />
        <div />
        <div />
      </div>
    </div>
  );
};
export default BaseSpinner;
