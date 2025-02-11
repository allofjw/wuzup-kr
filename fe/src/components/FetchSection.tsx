import Toggle from "./Toggle.tsx"; // Import the Toggle component

interface FetchSectionProps {
  fetchData: () => void;
  loading: boolean;
  message: string | null;
  index: boolean;
  setIndex: (index: number) => void;
  date: string;
  setDate: (date: string) => void;
  autoRefresh: boolean;
  setAutoRefresh: React.Dispatch<React.SetStateAction<boolean>>;
}

const FetchSection: React.FC<FetchSectionProps> = ({
  fetchData,
  loading,
  message,
  index,
  setIndex,
  date,
  setDate,
  autoRefresh,
  setAutoRefresh,
}: FetchSectionProps) => {
  return (
    <section className="relative wrapper">
      <form className="w-screen flex-wrap lg:w-max lg:flex-nowrap lg:absolute lg:right-12 flex flex-row gap-4 items-center bg-gradient-to-r from-slate-400 to-slate-800 rounded-md mx-4 lg:mx-0 my-4 p-2 min-w-[40vh]">
        <input
          type="date"
          value={`${new Date().getFullYear()}-${date.slice(0, 2)}-${date.slice(
            2
          )}`}
          onChange={(e) => {
            const selectedDate = new Date(e.target.value);
            const month = String(selectedDate.getMonth() + 1).padStart(2, "0");
            const day = String(selectedDate.getDate()).padStart(2, "0");
            setDate(`${month}${day}`);
          }}
          className="p-2 rounded-md"
        />
        <Toggle index={index} setIndex={setIndex} />
        <button
          onClick={fetchData}
          disabled={loading}
          className={`${
            loading ? "opacity-50 cursor-not-allowed" : "hover:bg-blue-600"
          } p-2 bg-blue-500 text-white rounded-md`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24"
            viewBox="0 96 960 960"
            width="24"
            fill={loading ? "#F0F0F0" : "#FFFFFF"}
          >
            <path d="M480 936q-150 0-255-105T120 576q0-150 105-255T480 216q94 0 172.5 46T780 384V256h60v240H600v-60h185q-44-82-118.5-131T480 276q-125 0-212.5 87.5T180 576q0 125 87.5 212.5T480 876q76 0 144.5-37.5T740 720h68q-41 106-134.5 173T480 936Z" />
          </svg>
        </button>
        <button
          type="button"
          onClick={() => setAutoRefresh((prev) => !prev)}
          className={`toggle-button ${
            autoRefresh ? "bg-red-400" : "bg-slate-400"
          }`}
        >
          <span>Auto</span>
        </button>
        <div className="lg:w-[20vw] overflow-hidden truncate text-white">
          {message}
        </div>
      </form>
    </section>
  );
};

export default FetchSection;
