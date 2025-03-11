import React, { useEffect, useState } from "react";
import "./TopicDisplay.css";

function TopicDisplay() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeYear, setActiveYear] = useState(null);
  const [activeCategory, setActiveCategory] = useState(null);
  const [scrolling, setScrolling] = useState(false);
  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await fetch("/lda_results.json");
        const categoryResponse = await fetch("/category_mappings.json");
        if (!response.ok || !categoryResponse.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        const categoryMappings = await categoryResponse.json();
        // Update the categories with human-readable names dynamically
        const updatedTopics = Object.keys(data).reduce((acc, year) => {
          acc[year] = Object.keys(data[year]).reduce((yearAcc, category) => {
            const humanReadableCategory =
              categoryMappings[category] || category; // fallback to original if not found
            yearAcc[humanReadableCategory] = data[year][category];
            return yearAcc;
          }, {});
          return acc;
        }, {});

        setTopics(updatedTopics);
      } catch (error) {
        setError("Failed to fetch topics.");
      } finally {
        setLoading(false);
      }
    };

    fetchTopics();
  }, []);

  // Handle scroll detection
  const handleScroll = () => {
    if (window.scrollY > 100) {
      setScrolling(true);
    } else {
      setScrolling(false);
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const handleYearClick = (year) => {
    setActiveYear(activeYear === year ? null : year);
    setActiveCategory(null); // Reset category when changing year
  };

  const handleCategoryClick = (category) => {
    setActiveCategory(activeCategory === category ? null : category);
    // Scroll to the top of the page when a category is selected
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (loading) {
    return <div className="loading-spinner">Loading...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="topic-display-container">
      <header className={`sticky-header ${scrolling ? "scrolled" : ""}`}>
        <h1>Topic Modeling Results</h1>
      </header>

      <div className="main-content">
        <div className="sidebar">
          <h3>Years</h3>
          <ul>
            {Object.keys(topics).map((year) => (
              <li key={year}>
                <button
                  className={`sidebar-button ${
                    activeYear === year ? "active" : ""
                  }`}
                  onClick={() => handleYearClick(year)}
                >
                  {year}
                </button>
                {activeYear === year && (
                  <ul className="category-list">
                    {Object.keys(topics[year]).map((category) => (
                      <li key={category}>
                        <button
                          className={`category-button ${
                            activeCategory === category ? "active" : ""
                          }`}
                          onClick={() => handleCategoryClick(category)}
                        >
                          {category}
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        </div>

        <div className="content">
          {activeYear && (
            <div className={`year-card ${scrolling ? "sticky" : ""}`}>
              <h2>{activeYear}</h2>
              {activeCategory && (
                <div className="category-card">
                  <h3>{activeCategory}</h3>
                  <div className="topics">
                    {topics[activeYear][activeCategory].map((topic) => (
                      <div key={topic.topic_idx} className="topic-card">
                        <p>
                          <strong>Topic Index:</strong> {topic.topic_idx}
                        </p>
                        <p>
                          <strong>Top Words:</strong>{" "}
                          {topic.top_words.join(", ")}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TopicDisplay;
