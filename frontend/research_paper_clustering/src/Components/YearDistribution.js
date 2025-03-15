import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const YearDistribution = () => {
  const [yearData, setYearData] = useState(null);
  useEffect(() => {
    fetch("year_distribution.json")
      .then((response) => response.json())
      .then((data) => setYearData(data))
      .catch((error) => {
        console.error("Error fetching the data", error);
      });
  }, []);
  if (!yearData) {
    return <div>Loading</div>;
  }
  const data = [
    { x: yearData["Years"], y: yearData["Year Counts"], type: "bar" },
  ];
  return (
    <div>
      <Plot data={data}></Plot>
    </div>
  );
};

export default YearDistribution;
