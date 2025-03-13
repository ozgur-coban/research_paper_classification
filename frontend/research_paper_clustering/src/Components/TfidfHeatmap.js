import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";
const TfidfHeatmap = () => {
  const [tfidfData, setTfidfData] = useState(null);
  useEffect(() => {
    fetch("/tfidf_distribution.json")
      .then((response) => response.json())
      .then((data) => setTfidfData(data))
      .catch((error) => console.error("Error fetching the data: ", error));
  }, []);
  if (!tfidfData) {
    return <div>Loading...</div>;
  }
  console.log(tfidfData);
  const data = [
    {
      x: tfidfData["Years"],
      y: tfidfData["Words"],
      z: tfidfData["TF-IDF Scores"],
      type: "heatmap",
      colorscale: "Viridis",
    },
  ];
  return (
    <Plot
      data={data}
      layout={{
        title: "TF-IDF Heatmap",
        xaxis: { title: "Years" },
        yaxis: { title: "Words" },
      }}
    ></Plot>
  );
};

export default TfidfHeatmap;
