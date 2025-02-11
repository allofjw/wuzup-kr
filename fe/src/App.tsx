import { useEffect, useState } from "react";
import "./App.css";
import Footer from "./components/common/Footer.tsx";
import Header from "./components/common/Header.tsx";
import ListSection from "./components/ListSection.tsx";
import FetchSection from "./components/FetchSection.tsx";
// @deno-types="@types/react"

export interface DataItem {
  comments: {
    id: number;
    content: string;
  }[];
  title: string;
}

function App() {
  const [data, setData] = useState<DataItem[] | null>(null);
  const [date, setDate] = useState(() => {
    const today = new Date();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    return `${month}${day}`;
  });
  const [message, setMessage] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [index, setIndex] = useState(1);

  const [autoRefresh, setAutoRefresh] = useState<boolean>(true);
  const [popupMsg, setPopupMsg] = useState<string>(
    "Automatic fetch successful!"
  );
  const [showPopup, setShowPopup] = useState<boolean>(false);

  const backendUrl = "https://wuzup-proxy.deno.dev/news";

  const fetchData = async () => {
    setLoading(true);

    try {
      const response = await fetch(backendUrl + `/${date}/${index}`);

      console.log("Status " + response.status);
      if (response.status === 204) {
        setData(null);
        setMessage("No content was returned");
        setResult("204 No Content was returned");
        return;
      } else if (response.status === 404) {
        setData(null);
        setMessage("Returned invalid entry or no data");
        setResult("404 Entry not found or missing");
        return;
      } else if (!response.ok) {

        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setData(data);
      setMessage("Fetch successful!");
      setResult("200 OK");
    } catch (error) {
      const errorMsg = String(error).slice(0, 50);

      console.error("Failed to fetch data:", errorMsg);
      setData(null);
      setMessage("Unknown error");
      setResult("Unknown error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {// Initial fetch on component mount
    if (!autoRefresh) return;

    fetchData().then(() => {
      if (data != null) {
        setPopupMsg("Initial fetch successful!");
      } else {
        setPopupMsg("Initial fetch failed: \n" + result);
      }
      setShowPopup(true);
      setTimeout(() => setShowPopup(false), 3000); // Hide popup after 3 seconds
    });

    const intervalId = setInterval(() => {
      const selectedDate = new Date();
      const month = String(selectedDate.getMonth() + 1).padStart(2, "0");
      const day = String(selectedDate.getDate()).padStart(2, "0");

      fetchData().then(() => {
        setDate(`${month}${day}`);

        const currentTime = new Date(); // Get the current date and time
        currentTime.setMinutes(currentTime.getMinutes() + 5);

        setMessage(`Next refresh in ${currentTime.toLocaleString()}`);

        if (data != null) {
          setPopupMsg("Automatic fetch successful!");
        } else {
          setPopupMsg("Last fetch failed: \n" + result);
        }

        setShowPopup(true);
        setTimeout(() => setShowPopup(false), 3000); // Hide popup after 3 seconds
      });
    }, 5 * 60 * 1000); // Fetch every 5 minutes

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, [autoRefresh, date, index]);

  return (
    <>
      <Header />
      <FetchSection
        fetchData={fetchData}
        loading={loading}
        message={message}
        index={index}
        setIndex={setIndex}
        date={date}
        setDate={setDate}
        autoRefresh={autoRefresh}
        setAutoRefresh={setAutoRefresh}
      />
      <ListSection data={data} loading={loading} />
      <Footer />
      {showPopup && <Popup message={popupMsg} />}
    </>
  );
}

function Popup({ message }: { message: string }) {
  return (
    <div className="popup">
      <div className="bg-gray-800 p-4 rounded shadow-lg max-w-[40vw] mx-auto transition-all duration-300">
        {message}
      </div>
    </div>
  );
}

export default App;
