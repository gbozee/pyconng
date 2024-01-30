import { css, cva } from "../../styled-system/css";
import { flex } from "../../styled-system/patterns";
import { button } from "../Button";
import logo from "./logo.png";

const Logo = () => {
  return (
    <a
      href="/"
      className={flex({
        cursor: "pointer",
        color: "white",
        direction: "row",
        gap: "12px",
        "& img": {
          width: "4rem",
          height: "4rem",
        },
      })}
    >
      <img src={logo} alt="logo" />
      <div
        className={css({
          textTransform: "uppercase",
        })}
      >
        <h1
          className={css({
            color: "#04A38A",
            fontSize: "28px",
            fontWeight: "700",
            letterSpacing: "1.12px",
          })}
        >
          PyCon
        </h1>
        <h2
          className={css({
            color: "#f4f0f0",
            fontSize: "16px",
          })}
        >
          Nigeria 2024
        </h2>
      </div>
    </a>
  );
};

type NavigationBarProps = {
  links: Array<{
    name: string;
    path: string;
  }>;
};
const NavigationBar = ({ links }: NavigationBarProps) => {
  return (
    <div
      className={flex({
        pt: "45px",
        justifyContent: "space-between",
        direction: {
          base: "column",
          lg: "row",
        },
      })}
    >
      <Logo />
      <ul
        className={flex({
          color: "white",
          borderRadius: "100px",
          gap: "34px",
          border: "1px solid rgba(244, 240, 240, 0.30)",
          padding: "16px 20px",
          textTransform: "uppercase",
        })}
      >
        {links.map((link) => (
          <li>
            <a href={link.path}>{link.name}</a>
          </li>
        ))}
      </ul>
      <div
        className={flex({
          gap: "12px",
        })}
      >
        <a className={button({})}>Login</a>
        <a
          className={button({
            visual: "primary",
          })}
        >
          Signup{" "}
        </a>
      </div>
    </div>
  );
};

export default NavigationBar;
