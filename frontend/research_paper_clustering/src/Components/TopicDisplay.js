import React, { useEffect, useState, useRef } from "react";
import "./TopicDisplay.css";

function TopicDisplay() {
  const [topics, setTopics] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeYear, setActiveYear] = useState(null);
  const [activeCategory, setActiveCategory] = useState(null);
  const [expandedCategories, setExpandedCategories] = useState({});
  const contentRef = useRef(null);

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

        // Convert category keys to human-readable names
        const updatedTopics = Object.keys(data).reduce((acc, year) => {
          acc[year] = Object.keys(data[year]).reduce((yearAcc, category) => {
            const humanReadableCategory =
              categoryMappings[category] || category;
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

  const handleYearClick = (year) => {
    setActiveYear(activeYear === year ? null : year);
    setActiveCategory(null);
    setExpandedCategories({});
  };

  const handleCategoryClick = (category) => {
    setActiveCategory(activeCategory === category ? null : category);
    if (contentRef.current) {
      contentRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  const toggleCategoryExpansion = (year) => {
    setExpandedCategories((prev) => ({
      ...prev,
      [year]: !prev[year],
    }));
  };

  if (loading) return <div className="loading-spinner">Loading...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="main-content">
      <div className="sidebar">
        <h3>Years</h3>
        <ul>
          {Object.keys(topics)
            .reverse()
            .map((year) => {
              const categories = Object.keys(topics[year]);
              const isExpanded = expandedCategories[year];
              const displayedCategories = isExpanded
                ? categories
                : categories.slice(0, 10);

              return (
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
                    <div className="category-list-container">
                      {displayedCategories.map((category) => (
                        <button
                          key={category}
                          className={`category-button ${
                            activeCategory === category ? "active" : ""
                          }`}
                          onClick={() => handleCategoryClick(category)}
                        >
                          {category}
                        </button>
                      ))}
                      {categories.length > 10 && (
                        <button
                          className="show-more-button"
                          onClick={() => toggleCategoryExpansion(year)}
                        >
                          {isExpanded ? "Show Less" : "Show More"}
                        </button>
                      )}
                    </div>
                  )}
                </li>
              );
            })}
        </ul>
      </div>

      <div className="content" ref={contentRef}>
        {activeYear && activeCategory && (
          <div className="category-card">
            <h2>
              {activeYear} - {activeCategory}
            </h2>
            <div className="topics">
              {topics[activeYear][activeCategory].map((topic) => (
                <div key={topic.topic_idx} className="topic-card">
                  <p>
                    <strong>Top TF-IDF, LDA Words:</strong>{" "}
                    {topic.top_words.join(", ")}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default TopicDisplay;
