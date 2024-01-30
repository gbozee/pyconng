import { cva } from "../styled-system/css";

export const button = cva({
  base: {
    padding: "16px 20px",
    borderRadius: "100px",
    border: "1px solid rgba(244, 240, 240, 0.30)",
    color: "white",
    cursor: "pointer",
    fontSize: "16px",
    fontWeight: "600",
    lineHeight: "24px",
  },
  variants: {
    visual: {
      primary: {
        background:
          "linear-gradient(200deg, rgba(244, 240, 240, 0.40) 1.18%, rgba(244, 240, 240, 0.00) 157.95%)",
      },
      default: {
        background: "transparent",
      },
      main: {
        background: "black",
      },
    },
  },
  defaultVariants: {
    visual: "default",
  },
});
