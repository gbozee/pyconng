import { PropsWithChildren } from "react";
import { css } from "../styled-system/css";

const AppContainer = ({ children }: PropsWithChildren) => {
  return (
    <main
      className={css({
        background: "#141615",
        backdropFilter: "blur(2px)",
      })}
    >
      {children}
    </main>
  );
};

export default AppContainer;
