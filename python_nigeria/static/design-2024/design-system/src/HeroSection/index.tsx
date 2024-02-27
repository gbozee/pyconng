import { css } from "../../styled-system/css";
import { flex } from "../../styled-system/patterns";

const HeroSection = () => {
  return (
    <div
      className={flex({
        py: "200px",
        color: "#F4F0F0",
        textAlign: "center",
        mx: "auto",
        maxWidth: "3xl",
        direction: "column",
      })}
    >
      <h4
        className={css({
          color: "#04A38A",
          backgroundClip: "text",
          fontSize: "24px",
          fontWeight: "600",
        })}
      >
        Calling all Pythonistas
      </h4>
      <h1
        className={css({
          fontSize: "48px",
          fontWeight: "600",
          textTransform: "uppercase",
        })}
      >
        Python Conference 2024
      </h1>
      <div
        className={css({
          mt: "12px",
          fontSize: "40px",
          fontWeight: "500",
          lineHeight: "normal",
        })}
      >
        <p>15.09 - 17.09</p>
        <p> Lagos, Nigeria</p>
      </div>
    </div>
  );
};

export default HeroSection;
