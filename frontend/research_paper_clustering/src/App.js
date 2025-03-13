import "./App.css";
import React from "react";
import TopicDisplay from "./Components/TopicDisplay";
import CategoryDistribution from "./Components/CategoryDistribution";
import TfidfHeatmap from "./Components/TfidfHeatmap";
function App() {
  return (
    <div className="App">
      <TopicDisplay></TopicDisplay>
      <CategoryDistribution></CategoryDistribution>
      <TfidfHeatmap></TfidfHeatmap>
    </div>
  );
}

export default App;
