import europe from "./europe.png";
import briefcase from "./briefcase.png";
import lightning from "./lightning-bolt.png";
import code from "./code.png";
import { css } from "../../styled-system/css";
import { container, flex } from "../../styled-system/patterns";
import { button } from "../Button";

const SponsorItem = ({ title, logo, body }: any) => {
  return (
    <div
      className={css({
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "12px",
        "& h3": {
          fontSize: "24px",
          fontWeight: "600",
          lineHeight: "32px",
          textAlign: "center",
        },
        "& p": {
          fontSize: "16px",
          lineHeight: "24px",
          textAlign: "center",
        },
      })}
    >
      <img src={logo} alt="logo" />
      <h3>{title}</h3>
      <p>{body}</p>
    </div>
  );
};

const sections = [
  {
    title: "React the right audience",
    logo: europe,
    body: `Lorem ipsum dolor sit amet consectetur. Diam mattis sit risus ultrices vivamus. Leo velit ut arcu et scelerisque netus varius. Cursus a facilisi turpis urna elementum velit fringilla risus scelerisque. Fringilla justo egestas sociis sem diam ante platea. Faucibus`,
  },
  {
    title: "React the right audience",
    logo: briefcase,
    body: `Lorem ipsum dolor sit amet consectetur. Diam mattis sit risus ultrices vivamus. Leo velit ut arcu et scelerisque netus varius. Cursus a facilisi turpis urna elementum velit fringilla risus scelerisque. Fringilla justo egestas sociis sem diam ante platea. Faucibus`,
  },
  {
    title: "React the right audience",
    logo: lightning,
    body: `Lorem ipsum dolor sit amet consectetur. Diam mattis sit risus ultrices vivamus. Leo velit ut arcu et scelerisque netus varius. Cursus a facilisi turpis urna elementum velit fringilla risus scelerisque. Fringilla justo egestas sociis sem diam ante platea. Faucibus`,
  },
];

const BecomeASponsor = () => {
  return (
    <section
      className={container({
        bg: "white",
        py: "73px",
        textAlign: "center",
        maxWidth: {
          base: "100%",
          md: "8xl",
        },
      })}
    >
      <h2
        className={css({
          color: "#000",
          fontSize: "32px",
          fontWeight: "600",
          lineHeight: "20px",
          mb: "60px",
        })}
      >
        Become a sponsor
      </h2>
      <img
        className={css({
          position: "absolute",
          width: "100px",
          height: "100px",
          top: "60px",
          right: 0,
        })}
        src={code}
        alt="code"
      />
      <div
        className={flex({
          gap: "24px",
          direction: {
            base: "column",
            lg: "row",
          },
        })}
      >
        {sections.map((section, index) => (
          <SponsorItem key={index} {...section} />
        ))}
      </div>
      <div
        className={css({
          mt: "60px",
        })}
      >
        <a
          className={button({
            visual: "main",
          })}
        >
          Sponsor PYCON
        </a>
      </div>
    </section>
  );
};

export default BecomeASponsor;
