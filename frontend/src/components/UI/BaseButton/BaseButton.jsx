import classes from "./BaseButton.module.css";

const BaseButton = (props) => {
  return (
    <button
      onClick={
        props.type === "button" || !props.type ? props.onClick : undefined
      }
      type={props.type ? props.type : "button"}
      className={
        classes[props.mode] + " " + classes.button + " " + classes[props.size]
      }
    >
      {props.children}
    </button>
  );
};

export default BaseButton;
