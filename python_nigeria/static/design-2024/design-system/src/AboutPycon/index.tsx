import { css } from "../../styled-system/css";
import { container } from "../../styled-system/patterns";
import code from "./code.png";
const AboutPycon = () => {
  return (
    <section
      className={css({
        bg: "#DCFCE7",
        position: "relative",
        pt: "50px",
        pb: "199px",
      })}
    >
      <div
        className={container({
          maxWidth: "8xl",
          textAlign: "center",
          "& img": {
            width: "100px",
            height: "100px",
          },
          "& h2": {
            fontSize: "48px",
            fontWeight: "700",
            lineHeight: "normal",
            mb: "12px",
          },
        })}
      >
        <h2>About PYCON</h2>
        <p
          className={css({
            color: "#B3BCC0",
          })}
        >
          The PyConNG 2024 is the largest annual gathering of Python geeks in
          Nigeria. It is organised by members of the Python Users Nigeria Group,
          a nonprofit organisation dedicated to advancing the Python community
          in Nigeria. Python developers get to learn, network and collaborate
          during the workshops, it’s a place to be!
        </p>
        <img src={code} alt="" />
        <iframe
          className={css({
            mx: "auto",
            width: "420px",
            height: "345px",
          })}
          src="https://www.youtube.com/embed/tgbNymZ7vqY"
        ></iframe>
      </div>
    </section>
  );
};

export default AboutPycon;
