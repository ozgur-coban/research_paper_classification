import "./css/App.css";
import React from "react";
import TopicDisplay from "./Components/TopicDisplay";
import CategoryDistribution from "./Components/CategoryDistribution";
import YearDistribution from "./Components/YearDistribution";
import TfidfHeatmap from "./Components/TfidfHeatmap";
import { useState } from "react";
import { Tabs, Tab, Box } from "@mui/material";

function App() {
  const [tabIndex, setTabIndex] = useState(0); // 0 = Topic Display, 1 = Graphs

  return (
    <div className="App">
      {/* Tabs at the top */}
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs
          value={tabIndex}
          onChange={(e, newValue) => setTabIndex(newValue)}
        >
          <Tab label="Topic Display" />
          <Tab label="Graphs" />
        </Tabs>
      </Box>

      {/* Show TopicDisplay if tabIndex is 0 */}
      {tabIndex === 0 && <TopicDisplay />}

      {/* Show graphs in a grid if tabIndex is 1 */}
      {tabIndex === 1 && (
        <div className="dashboard">
          <div className="grid-container">
            <div className="grid-item">
              <CategoryDistribution />
            </div>
            <div className="grid-item">
              <YearDistribution />
            </div>
            <div className="grid-item full-width">
              <TfidfHeatmap />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
