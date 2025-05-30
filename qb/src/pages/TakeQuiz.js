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

  useEffect(() => {
    fetch(`/api/quiz/${quizId}`)
      .then((res) => res.json())
      .then((data) => {
        setQuiz(data.quiz);
        setQuestions(data.questions);
        setTimeLeft(data.quiz.time_duration * 60);
      });
  }, [quizId]);

 
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

 
  const submitQuiz = useCallback(() => {
    if (quizSubmitted) return;
    setQuizSubmitted(true);

    const payload = {
      quiz_id: quizId,
      answers,
    };

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

 
  const forceSubmitZero = useCallback(() => {
    if (quizSubmitted) return;
    setQuizSubmitted(true);

    fetch("/api/quiz/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quiz_id: quizId, force_zero: true }),
    }).finally(() => navigate("/dashboard"));
  }, [quizId, navigate, quizSubmitted]);

  // Fullscreen logic
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

    document.addEventListener("keydown", handleKey);
    document.addEventListener("visibilitychange", handleVisibility);
    document.addEventListener("contextmenu", handleContext);

    return () => {
      document.removeEventListener("keydown", handleKey);
      document.removeEventListener("visibilitychange", handleVisibility);
      document.removeEventListener("contextmenu", handleContext);
    };
  }, [quizSubmitted, forceSubmitZero]);

  const handleStart = () => {
    if (!window.confirm("⚠️ Start quiz in full-screen mode? Any tab switch or fullscreen exit will auto-submit with 0 score.")) return;

    const doc = document.documentElement;
    if (doc.requestFullscreen) doc.requestFullscreen();

    setStarted(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (window.confirm("Are you sure you want to submit?")) {
      submitQuiz();
    }
  };

  const handleOptionChange = (questionId, value) => {
    setAnswers({ ...answers, [questionId]: value });
  };

  if (!quiz) return <p>Loading...</p>;

  return (
    <div className="container">
      <h2>{quiz.title}</h2>
      <p><strong>Subject:</strong> {quiz.chapter.subject.name}</p>
      <p><strong>Chapter:</strong> {quiz.chapter.name}</p>
      <p><strong>Time Left:</strong> {Math.floor(timeLeft / 60)}m {timeLeft % 60}s</p>

      {!started && <button className="btn btn-primary" onClick={handleStart}>Start Quiz</button>}

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
          <button type="submit" className="btn btn-success">Submit Quiz</button>
        </form>
      )}
    </div>
  );
};

export default QuizPage;
