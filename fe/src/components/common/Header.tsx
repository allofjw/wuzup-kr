import FC from "react";

const Header: FC = () => {
  return (
    <section>
      <div className="fixed w-full top-0 z-30">
        <div className="wrapper">
          <div className="h-16 w-full flex flex-row items-center justify-between bg-slate-300 p-4">
            <div>
              <h2>WUZUP KR</h2>
            </div>
            <div>
              <ul className="flex flex-row gap-4">
                <a href="/">
                  <li>Home</li>
                </a>
                <a href="/credits/">
                  <li>Credits</li>
                </a>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div className="h-16 w-full"></div>
    </section>
  );
};

export default Header;
