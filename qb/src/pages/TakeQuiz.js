import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const QuizPage = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();

  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [started, setStarted] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);
  const [quizSubmitted, setQuizSubmitted] = useState(false);

  // 🔁 Shuffle helper
  const shuffleArray = (array) => {
    return array.sort(() => Math.random() - 0.5);
  };

  // 🚀 Fetch Quiz Data & Shuffle Questions + Options
  useEffect(() => {
    fetch(`/api/quiz/${quizId}`)
      .then((res) => res.json())
      .then((data) => {
        setQuiz(data.quiz);
        const shuffledQuestions = shuffleArray(data.questions).map((q) => ({
          ...q,
          options: Object.fromEntries(shuffleArray(Object.entries(q.options))),
        }));
        setQuestions(shuffledQuestions);
        setTimeLeft(data.quiz.time_duration * 60);
      });

    // ⏪ Load answers from localStorage (if exists)
    const saved = localStorage.getItem(`answers_${quizId}`);
    if (saved) setAnswers(JSON.parse(saved));
  }, [quizId]);

  // ⏳ Timer Logic
  useEffect(() => {
    if (!started || quizSubmitted) return;
    if (timeLeft <= 0) {
      alert("⏰ Time is up! Submitting quiz...");
      submitQuiz();
      return;
    }
    const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
    return () => clearTimeout(timer);
  }, [timeLeft, started, quizSubmitted]);

  // ✅ Submit Quiz
  const submitQuiz = useCallback(() => {
    if (quizSubmitted) return;
    setQuizSubmitted(true);
    const payload = { quiz_id: quizId, answers };

    fetch("/api/quiz/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        alert(`✅ ${data.message}\nYour Score: ${data.score}`);
        navigate("/dashboard");
      })
      .catch((err) => {
        console.error("Submission error:", err);
        alert("An error occurred. Please try again.");
      });
  }, [quizId, answers, navigate, quizSubmitted]);

  // ⛔️ Force Submit 0 if violated
  const forceSubmitZero = useCallback(() => {
    if (quizSubmitted) return;
    setQuizSubmitted(true);
    fetch("/api/quiz/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quiz_id: quizId, force_zero: true }),
    }).finally(() => navigate("/dashboard"));
  }, [quizId, navigate, quizSubmitted]);

  // 🖥️ Fullscreen Exit Detection
  useEffect(() => {
    const handleExit = () => {
      if (!document.fullscreenElement && !quizSubmitted) {
        forceSubmitZero();
      }
    };
    document.addEventListener("fullscreenchange", handleExit);
    return () => {
      document.removeEventListener("fullscreenchange", handleExit);
    };
  }, [quizSubmitted, forceSubmitZero]);

  // 🛡️ Anti-cheat: disable inspect, visibility change, context menu
  useEffect(() => {
    const handleKey = (e) => {
      if (
        e.keyCode === 123 ||
        (e.ctrlKey && e.shiftKey && ['I', 'J'].includes(e.key)) ||
        (e.ctrlKey && e.key === 'U')
      ) {
        e.preventDefault();
      }
    };
    const handleVisibility = () => {
      if (document.hidden && !quizSubmitted) {
        forceSubmitZero();
      }
    };
    const handleContext = (e) => e.preventDefault();
    const handleCopyPaste = (e) => e.preventDefault();

    document.addEventListener("keydown", handleKey);
    document.addEventListener("visibilitychange", handleVisibility);
    document.addEventListener("contextmenu", handleContext);
    document.addEventListener("copy", handleCopyPaste);
    document.addEventListener("paste", handleCopyPaste);

    return () => {
      document.removeEventListener("keydown", handleKey);
      document.removeEventListener("visibilitychange", handleVisibility);
      document.removeEventListener("contextmenu", handleContext);
      document.removeEventListener("copy", handleCopyPaste);
      document.removeEventListener("paste", handleCopyPaste);
    };
  }, [quizSubmitted, forceSubmitZero]);

  // 🟢 Start Quiz
  const handleStart = () => {
    if (!window.confirm("⚠️ Start quiz in full-screen mode? Any tab switch or fullscreen exit will auto-submit with 0 score.")) return;
    const doc = document.documentElement;
    if (doc.requestFullscreen) doc.requestFullscreen();
    setStarted(true);
  };

  // 📤 Manual Submit
  const handleSubmit = (e) => {
    e.preventDefault();
    if (window.confirm("Are you sure you want to submit?")) {
      submitQuiz();
    }
  };

  // 📝 Option Select
  const handleOptionChange = (questionId, value) => {
    const updated = { ...answers, [questionId]: value };
    setAnswers(updated);
    localStorage.setItem(`answers_${quizId}`, JSON.stringify(updated)); // 💾 Save to localStorage
  };

  // 📁 Export Answers
  const exportAnswers = () => {
    const blob = new Blob([JSON.stringify(answers, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "quiz_answers.json";
    link.click();
  };

  if (!quiz) return <p>Loading...</p>;

  return (
    <div className="container py-4" style={{ maxWidth: "800px" }}>
      <h2>{quiz.title}</h2>
      <p><strong>Subject:</strong> {quiz.chapter.subject.name}</p>
      <p><strong>Chapter:</strong> {quiz.chapter.name}</p>
      <p><strong>Time Left:</strong> {Math.floor(timeLeft / 60)}m {timeLeft % 60}s</p>

      {/* ✅ Visual Answered Tracker */}
      <div className="mb-3">
        {questions.map((q, index) => (
          <span
            key={q.id}
            className={`badge me-1 ${answers[q.id] ? 'bg-success' : 'bg-secondary'}`}
          >
            Q{index + 1}
          </span>
        ))}
      </div>

      {/* 🔁 Time Progress Bar */}
      <div className="progress mb-3">
        <div
          className="progress-bar"
          role="progressbar"
          style={{ width: `${(timeLeft / (quiz.time_duration * 60)) * 100}%` }}
          aria-valuenow={(timeLeft / (quiz.time_duration * 60)) * 100}
          aria-valuemin="0"
          aria-valuemax="100"
        >
          {Math.floor(timeLeft / 60)}:{String(timeLeft % 60).padStart(2, '0')}
        </div>
      </div>

      {!started && (
        <button className="btn btn-primary" onClick={handleStart}>
          Start Quiz
        </button>
      )}

      {started && (
        <form onSubmit={handleSubmit}>
          {questions.map((q, index) => (
            <div className="mb-4" key={q.id}>
              <p><strong>{index + 1}. {q.question_text}</strong></p>
              {Object.entries(q.options).map(([key, val]) => (
                <div className="form-check" key={key}>
                  <input
                    type="radio"
                    className="form-check-input"
                    name={`question_${q.id}`}
                    id={`q${q.id}_${key}`}
                    value={key}
                    checked={answers[q.id] === key}
                    onChange={() => handleOptionChange(q.id, key)}
                    required
                  />
                  <label htmlFor={`q${q.id}_${key}`} className="form-check-label">
                    {key}. {val}
                  </label>
                </div>
              ))}
            </div>
          ))}
          {/* 📥 Export and Submit Buttons */}
          <div className="d-flex gap-2">
            <button type="button" className="btn btn-secondary" onClick={exportAnswers}>
              Download Answers
            </button>
            <button type="submit" className="btn btn-success">
              Submit Quiz
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default QuizPage;
