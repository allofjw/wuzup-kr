import Footer from "./components/common/Footer.tsx";
import Header from "./components/common/Header.tsx";
import Credits from "./components/credits/Credits.tsx";
// @deno-types="@types/react"
function CreditsApp() {
  return (
    <>
      <Header />
      <Credits />
      <Footer />
    </>
  );
}

export default CreditsApp;
