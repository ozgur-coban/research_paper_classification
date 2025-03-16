import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

function CategoryDistribution() {
  const [categoryData, setCategoryData] = useState(null);
  const [categoryMappings, setCategoryMappings] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        // Fetch both datasets in parallel
        const [categoryResponse, mappingsResponse] = await Promise.all([
          fetch("/category_distribution.json"),
          fetch("/category_mappings.json"),
        ]);

        if (!categoryResponse.ok || !mappingsResponse.ok) {
          throw new Error("Network response was not ok");
        }

        const categoryData = await categoryResponse.json();
        const mappingsData = await mappingsResponse.json();

        setCategoryData(categoryData);
        setCategoryMappings(mappingsData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    fetchData();
  }, []);

  if (!categoryData || !categoryMappings) {
    return <div>Loading...</div>;
  }

  // Prepare data for Plotly with hover text
  const shortNames = categoryData["CS Subcategories"];
  const fullNames = shortNames.map(
    (shortName) => categoryMappings[shortName] || shortName
  );

  const data = [
    {
      x: shortNames, // Keep short names on X-axis
      y: categoryData["Number of Papers"],
      type: "bar",
      marker: { color: "#1f77b4", line: { color: "#000", width: 1 } },
      text: fullNames, // Full names for hover text
      hoverinfo: "text+y", // Show full name + number of papers on hover
    },
  ];

  const layout = {
    title: { text: "Top CS Subcategories in ArXiv Dataset" },
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
