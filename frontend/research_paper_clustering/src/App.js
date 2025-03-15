import "./App.css";
import React from "react";
import TopicDisplay from "./Components/TopicDisplay";
import CategoryDistribution from "./Components/CategoryDistribution";
import YearDistribution from "./Components/YearDistribution";
import TfidfHeatmap from "./Components/TfidfHeatmap";
function App() {
  return (
    <div className="App">
      <TopicDisplay></TopicDisplay>
      <CategoryDistribution></CategoryDistribution>
      <YearDistribution></YearDistribution>
      <TfidfHeatmap></TfidfHeatmap>
    </div>
  );
}

export default App;
