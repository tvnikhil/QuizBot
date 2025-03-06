import React, { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "github-markdown-css/github-markdown.css";
import "./App.css";

function App() {
  const [quiz, setQuiz] = useState(null);
  const [qa, setQa] = useState(null);
  const [loading, setLoading] = useState(false);
  const [qaLoading, setQaLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("quiz");

  // Input states
  const [quizTopic, setQuizTopic] = useState("");
  const [qaQuestion, setQaQuestion] = useState("");

  // Store selected answers
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [answerFeedback, setAnswerFeedback] = useState({});

  // Fetch quiz
  const fetchQuiz = async () => {
    if (!quizTopic) return;
    setLoading(true);
    setError(null);
    setActiveTab("quiz");

    try {
      const response = await axios.post(
        // "/api/generate_quiz",
        // "http://34.174.53.242:8000/generate_quiz",
        "http://127.0.0.1:8000/generate_quiz",
        { text: quizTopic },
        { headers: { "Content-Type": "application/json" }, timeout: 120000 }
      );
      setQuiz(response.data.finalResponse);
      setSelectedAnswers({});
      setAnswerFeedback({});
    } catch (err) {
      console.error("Error fetching quiz:", err);
      setError(err.response?.data?.detail || "Failed to fetch quiz.");
    } finally {
      setLoading(false);
    }
  };

  // Fetch QA
  const getAnswer = async () => {
    if (!qaQuestion) return;
    setQaLoading(true);
    setError(null);
    setActiveTab("qa");

    try {
      const response = await axios.post(
        // "/api/open_ended",
        // "http://34.174.53.242:8000/open_ended",
        "http://127.0.0.1:8000/open_ended",
        { text: qaQuestion },
        { headers: { "Content-Type": "application/json" }, timeout: 120000 }
      );
      setQa(response.data.finalResponse);
    } catch (err) {
      console.error("Error fetching answer:", err);
      setError(err.response?.data?.detail || "Failed to fetch answer.");
    } finally {
      setQaLoading(false);
    }
  };

  // Handle user selection
  const handleOptionSelect = (questionIndex, option) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionIndex]: option,
    });
  };

  // Check if the selected answer is correct
  const checkAnswer = (questionIndex, correctAnswer) => {
    const selectedAnswer = selectedAnswers[questionIndex];
    if (!selectedAnswer) return;

    if (selectedAnswer === correctAnswer) {
      setAnswerFeedback({
        ...answerFeedback,
        [questionIndex]: "✅ Correct!",
      });
    } else {
      setAnswerFeedback({
        ...answerFeedback,
        [questionIndex]: `❌ Incorrect! Correct answer: ${correctAnswer}`,
      });
    }
  };

  return (
    <div className="app">
      {/* Tab Buttons */}
      <div className="tab-container">
        <button
          className={`tab-button ${activeTab === "quiz" ? "active" : ""}`}
          onClick={() => setActiveTab("quiz")}
        >
          MCQ Quiz
        </button>
        <button
          className={`tab-button ${activeTab === "qa" ? "active" : ""}`}
          onClick={() => setActiveTab("qa")}
        >
          Question-Answer
        </button>
      </div>

      {/* Quiz Section */}
      {activeTab === "quiz" && (
        <div className="quiz-section">
          <h2>Generate MCQs based on topic</h2>
          <input
            type="text"
            value={quizTopic}
            onChange={(e) => setQuizTopic(e.target.value)}
            placeholder="Enter topic for quiz..."
            className="input-box"
          />
          <button
            className="tab-button"
            onClick={fetchQuiz}
            disabled={loading || !quizTopic}
          >
            {loading ? "Loading..." : "Generate Quiz"}
          </button>

          {error && (
            <p
              className="error-text"
              style={{ color: "#d32f2f", fontWeight: "bold" }}
            >
              {error}
            </p>
          )}

          {quiz && (
            <div className="quiz-container">
              <h3>Quiz Questions</h3>
              <ol>
                {quiz.quiz.mcqs.map((mcq, index) => (
                  <li key={index} className="quiz-item">
                    <p>
                      <strong>{mcq.question_text}</strong>
                    </p>
                    {/* Inline styling to remove bullet points */}
                    <ul
                      style={{ listStyleType: "none", padding: 0, margin: 0 }}
                    >
                      {mcq.options.map((option, i) => (
                        <li key={i}>
                          <label>
                            <input
                              type="radio"
                              name={`question-${index}`}
                              value={option}
                              checked={selectedAnswers[index] === option}
                              onChange={() => handleOptionSelect(index, option)}
                            />
                            {option}
                          </label>
                        </li>
                      ))}
                    </ul>
                    <br />
                    <button
                      className="tab-button"
                      onClick={() => checkAnswer(index, mcq.correct_answer)}
                    >
                      Check Answer
                    </button>
                    {answerFeedback[index] && (
                      <p
                        className="feedback"
                        style={{ marginTop: "10px", fontWeight: "bold" }}
                      >
                        {answerFeedback[index]}
                      </p>
                    )}
                  </li>
                ))}
              </ol>
            </div>
          )}
        </div>
      )}

      {/* QA Section */}
      {activeTab === "qa" && (
        <div className="qa-section">
          <h2>Type a topic required for explanation</h2>
          <input
            type="text"
            value={qaQuestion}
            onChange={(e) => setQaQuestion(e.target.value)}
            placeholder="Enter your topic..."
            className="input-box"
          />
          <button
            className="tab-button"
            onClick={getAnswer}
            disabled={qaLoading || !qaQuestion}
          >
            {qaLoading ? "Loading..." : "Get Answer"}
          </button>

          {error && (
            <p
              className="error-text"
              style={{ color: "#d32f2f", fontWeight: "bold" }}
            >
              {error}
            </p>
          )}

          {qa && (
            <div className="answer-container">
              <h3>Answer</h3>
              <div
                className="markdown-body"
                style={{ backgroundColor: "white", color: "black" }}
              >
                <ReactMarkdown>{qa.answer}</ReactMarkdown>
              </div>

              {qa.sources?.length > 0 && (
                <div className="sources-container">
                  <h3>Sources</h3>
                  <ul>
                    {qa.sources.map((source, index) => (
                      <li key={index}>{source}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
