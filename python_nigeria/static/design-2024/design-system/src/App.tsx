import "@fontsource/montserrat";
import NavigationBar from "./NavigationBar";
import AppContainer from "./AppContainer";
import { container } from "../styled-system/patterns";
import HeroSection from "./HeroSection";
import BecomeASponsor from "./BecomeASponsor";
import AboutPycon from "./AboutPycon";
import WorldBestPractices from "./WorldBestPractice";
import Footer from "./Footer";
import JoinTheCommunity from "./JoinTheCommunity";
import FAQ from "./FAQ";

function App() {
  return (
    <>
      <AppContainer>
        <nav
          className={container({
            maxWidth: {
              base: "100%",
              lg: "8xl",
            },
          })}
        >
          <NavigationBar
            links={[
              {
                name: "Home",
                path: "/",
              },
              {
                name: "Code of Conduct",
                path: "/code-of-conduct",
              },
              {
                name: "Sponsorship",
                path: "/sponsorship",
              },
              {
                name: "Speak at PYCON",
                options: [
                  {
                    name: "Talks",
                    path: "/talks",
                  },
                  {
                    name: "Workshops",
                    path: "/workshops",
                  },
                ],
              },
            ]}
          />
        </nav>
        <HeroSection />
      </AppContainer>
      <BecomeASponsor />
      <AboutPycon />
      <WorldBestPractices />
      <FAQ />
      <JoinTheCommunity />
      <Footer />
    </>
  );
}

export default App;
