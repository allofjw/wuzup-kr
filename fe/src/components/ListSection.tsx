import FC from "react";
import KeywordList from "./KeywordList.tsx";
import { DataItem } from "../App.tsx";

interface ListSectionProps {
  data: DataItem[] | null;
  loading: boolean;
}

const ListSection: FC = ({ data, loading }: ListSectionProps) => {
  return (
    <section>
      <div className="my-4">
        <div className="wrapper min-h-[66vh] overflow-x-scroll">
          {data ? (
            <>
              {data.slice(0, 5).map((item, index) => (
                <KeywordList
                  comments={item.comments}
                  title={item.title}
                  key={index}
                />
              ))}
            </>
          ) : (
            !loading && <div className="mx-auto">No data available</div>
          )}
        </div>
      </div>
      {/* <div>
        <h2>Debugging:</h2>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div> */}
    </section>
  );
};

export default ListSection;
