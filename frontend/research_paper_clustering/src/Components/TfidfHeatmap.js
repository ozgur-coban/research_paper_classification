import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";
const TfidfHeatmap = () => {
  const [tfidfData, setTfidfData] = useState(null);
  const [selectedRange, setSelectedRange] = useState("2015-2025");
  useEffect(() => {
    fetch("/tfidf_distribution.json")
      .then((response) => response.json())
      .then((data) => setTfidfData(data))
      .catch((error) => console.error("Error fetching the data: ", error));
  }, []);
  if (!tfidfData) {
    return <div>Loading...</div>;
  }
  const timeRanges = [
    { start: 1994, value: "1994-2005", end: 2005 },
    { start: 2005, value: "2005-2015", end: 2015 },
    { start: 2015, value: "2015-2025", end: 2025 },
  ];
  const selectedTimeRange = timeRanges.find(
    (range) => range.value === selectedRange
  );
  const filteredIndices = tfidfData["Years"]
    .map((year, i) =>
      year >= selectedTimeRange.start && year < selectedTimeRange.end ? i : -1
    )
    .filter((i) => i !== -1);

  const heatmapData = [
    {
      x: filteredIndices.map((i) => tfidfData["Years"][i]), // Years in this range
      y: filteredIndices.map((i) => tfidfData["Words"][i]), // Words in this range
      z: filteredIndices.map((i) => tfidfData["TF-IDF Scores"][i]), // TF-IDF scores
      type: "heatmap",
      colorscale: "Viridis",
    },
  ];

  return (
    <div>
      <Plot
        data={heatmapData}
        layout={{
          title: `TF-IDF Heatmap (${selectedTimeRange.start} - ${selectedTimeRange.end})`,
          xaxis: { title: "Year" },
          yaxis: { title: "Words" },
        }}
      />
      <label>Select Year Range: </label>
      <select
        value={selectedRange}
        onChange={(e) => setSelectedRange(e.target.value)}
      >
        {timeRanges.map((range) => (
          <option key={range.value} value={range.value}>
            {range.value}
          </option>
        ))}
      </select>
    </div>
  );
};

export default TfidfHeatmap;
