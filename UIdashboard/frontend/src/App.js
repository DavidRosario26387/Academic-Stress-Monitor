import React, { useEffect, useState } from "react";
import { Chart } from "react-google-charts";
import axios from "axios";

function App() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios
      .get("https://dashboard-backend-elzh.onrender.com/api/logs")
      .then((res) => setLogs(res.data))
      .catch((err) => console.error(err));
  }, []);

  // === Metrics ===
  const totalMessages = logs.length;
  const stressedMessages = logs.filter((l) => l.Stress_label === "Stressed");
  const stressedCount = stressedMessages.length;
  const notStressedCount = totalMessages - stressedCount;

  const severityCounts = [
    stressedMessages.filter((l) => l.Stress_category === "Low").length,
    stressedMessages.filter((l) => l.Stress_category === "Medium").length,
    stressedMessages.filter((l) => l.Stress_category === "High").length,
  ];

  const keywordFrequency = {};
  stressedMessages.forEach((l) => {
    if (l.Stress_Reason) {
      keywordFrequency[l.Stress_Reason] =
        (keywordFrequency[l.Stress_Reason] || 0) + 1;
    }
  });

  // === Prepare sorted data for stress reasons ===
  const sortedKeywordData = [
    ["Reason", "Count"]
  ].concat(
    Object.entries(keywordFrequency)
      .sort((a, b) => b[1] - a[1])
      .map(([reason, count]) => [reason, count])
  );

  return (
    <div
      style={{
        padding: "30px",
        maxWidth: "1400px",
        margin: "0 auto",
        fontFamily: "Segoe UI, Roboto, sans-serif",
      }}
    >
      <h1 style={{ textAlign: "center", marginBottom: "10px" }}>
        Stress Detection Dashboard
      </h1>
      <p style={{ textAlign: "center", color: "#555" }}>
        Total messages analyzed: <b>{totalMessages}</b> | Stressed:{" "}
        <b>{stressedCount}</b>
      </p>

      {/* Charts Row 1 */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "40px",
          marginTop: "40px",
        }}
      >
        {/* Pie Chart: Stressed vs Non-Stressed */}
        <div
          style={{
            background: "#f5f5f5",
            borderRadius: "16px",
            padding: "20px",
            boxShadow: "0 3px 10px rgba(0,0,0,0.1)",
          }}
        >
          <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
            Stressed vs Non-Stressed
          </h2>
          <Chart
            chartType="PieChart"
            data={[
              ["Label", "Count"],
              ["Stressed", stressedCount],
              ["Not Stressed", notStressedCount],
            ]}
            options={{
              title: "Stress Distribution",
              pieHole: 0.4,
              slices: {
                0: { color: "#FF6384" },
                1: { color: "#36A2EB" },
              },
              legend: { position: "bottom" },
            }}
            width="100%"
            height="400px"
          />
        </div>

        {/* Column Chart: Stress Severity */}
        <div
          style={{
            background: "#f5f5f5",
            borderRadius: "16px",
            padding: "20px",
            boxShadow: "0 3px 10px rgba(0,0,0,0.1)",
          }}
        >
          <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
            Stress Severity Distribution
          </h2>
          <Chart
            chartType="ColumnChart"
            data={[
              ["Severity", "Messages", { role: "style" }],
              ["Low", severityCounts[0], "#36A2EB"],
              ["Medium", severityCounts[1], "#FFCE56"],
              ["High", severityCounts[2], "#FF6384"],
            ]}
            options={{
              title: "Severity Levels",
              hAxis: { title: "Severity" },
              vAxis: { title: "Messages" },
              legend: "none",
            }}
            width="100%"
            height="400px"
          />
        </div>
      </div>

      {/* Charts Row 2: Stress Reasons */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "40px",
          marginTop: "40px",
        }}
      >
        {/* Bar Chart: Top Stress Reasons */}
        <div
          style={{
            background: "#f5f5f5",
            borderRadius: "16px",
            padding: "30px",
            boxShadow: "0 3px 10px rgba(0,0,0,0.1)",
            minHeight: "450px",
          }}
        >
          <h2 style={{ textAlign: "center", marginBottom: "30px" }}>
            Top Stress Reasons
          </h2>
          <Chart
            chartType="BarChart"
            data={sortedKeywordData}
            options={{
              title: "Top Stress Reasons",
              chartArea: { width: "60%" },
              hAxis: { title: "Count", minValue: 0 },
              vAxis: { title: "Reason" },
              colors: ["#4285F4"],
            }}
            width="100%"
            height="400px"
          />
        </div>

        {/* Pie Chart: Stress Reasons */}
        <div
          style={{
            background: "#f5f5f5",
            borderRadius: "16px",
            padding: "30px",
            boxShadow: "0 3px 10px rgba(0,0,0,0.1)",
            minHeight: "450px",
          }}
        >
          <h2 style={{ textAlign: "center", marginBottom: "30px" }}>
            Stress Reasons Distribution
          </h2>
          <Chart
            chartType="PieChart"
            data={sortedKeywordData}
            options={{
              title: "Stress Reasons",
              pieHole: 0.4,
              legend: { position: "right" },
            }}
            width="100%"
            height="400px"
          />
        </div>
      </div>
    </div>
  );
}

export default App;
