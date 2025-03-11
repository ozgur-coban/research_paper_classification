import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

function CategoryDistribution() {
  const [categoryData, setCategoryData] = useState(null);
  useEffect(() => {
    // Fetch the JSON data from the public folder
    fetch("/category_distribution.json")
      .then((response) => response.json())
      .then((data) => setCategoryData(data))
      .catch((error) => console.error("Error fetching the data: ", error));
  }, []);

  // Render the plot only when data is available
  if (!categoryData) {
    return <div>Loading...</div>;
  }

  // Prepare data for Plotly
  const data = [
    {
      x: categoryData["CS Subcategories"],
      y: categoryData["Number of Papers"],
      type: "bar",
      marker: {
        color: "#1f77b4", // Optional color customization
      },
    },
  ];

  // Layout customization for the chart
  const layout = {
    title: "Top CS Subcategories in ArXiv Dataset",
    xaxis: {
      title: "CS Subcategories",
      tickangle: 45,
    },
    yaxis: {
      title: "Number of Papers",
    },
  };

  return (
    <div>
      <Plot data={data} layout={layout} />
    </div>
  );
}

export default CategoryDistribution;
