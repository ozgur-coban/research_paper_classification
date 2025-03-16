import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const YearDistribution = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/year_distribution.json")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error("Error fetching data: ", error));
  }, []);

  if (!data) {
    return <div>Loading...</div>;
  }

  return (
    <Plot
      data={[
        {
          x: data["Years"], // Years
          y: data["Year Counts"], // Number of papers per year
          type: "scatter",
          mode: "markers",
          marker: { opacity: 0.7, size: 5, color: "blue" },
        },
      ]}
      layout={{
        title: { text: "Number of Papers Published Over the Years" },
        xaxis: { title: "Year" },
        yaxis: { title: "Number of Papers" },
      }}
    />
  );
};

export default YearDistribution;
