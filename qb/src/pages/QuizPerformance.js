import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Container, Table, Button, Badge, Spinner, Alert } from "react-bootstrap";

const QuizPerformance = () => {
  const { quizAttemptId } = useParams();
  const navigate = useNavigate();

  const [score, setScore] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [userAnswers, setUserAnswers] = useState({});
  const [loading, setLoading] = useState(true); // ⏳ Loading state
  const [error, setError] = useState(null); // ❌ Error state

  // 🔁 Fetch quiz result on component mount
  useEffect(() => {
    fetch(`/api/quiz-result/${quizAttemptId}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch quiz result");
        return res.json();
      })
      .then((data) => {
        setScore(data.score);
        setQuestions(data.questions);
        setUserAnswers(data.user_answers);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching quiz result:", err);
        setError("Unable to load quiz performance. Please try again.");
        setLoading(false);
      });
  }, [quizAttemptId]);

  // 🔒 Ensure null safety
  const getAnswerBadge = (userAnswer, correctAnswer) => {
    if (!userAnswer || userAnswer === "Not Answered") {
      return <Badge bg="secondary">Not Answered</Badge>;
    }

    return userAnswer === correctAnswer ? (
      <Badge bg="success">{userAnswer}</Badge>
    ) : (
      <Badge bg="danger">{userAnswer}</Badge>
    );
  };

  return (
    <Container className="mt-4">
      <h2 className="mb-3">📊 Quiz Performance</h2>

      {/* ⏳ Show loading spinner */}
      {loading && (
        <div className="text-center my-4">
          <Spinner animation="border" role="status" />
          <p className="mt-2">Fetching your quiz results...</p>
        </div>
      )}

      {/* ❌ Show error if any */}
      {error && (
        <Alert variant="danger" className="text-center">
          {error}
        </Alert>
      )}

      {/* ✅ Render score and result table */}
      {!loading && !error && (
        <>
          <Alert variant="info">
            <strong>Total Score:</strong> {score?.total_score ?? "N/A"}
          </Alert>

          <Table bordered responsive hover className="shadow-sm">
            <thead className="table-dark">
              <tr>
                <th>Question</th>
                <th>Your Answer</th>
                <th>Correct Answer</th>
              </tr>
            </thead>
            <tbody>
              {questions.map((question) => {
                const userAnswer = userAnswers[question.id] || "Not Answered";

                return (
                  <tr key={question.id}>
                    <td style={{ whiteSpace: "pre-wrap" }}>
                      {question.question_text}
                    </td>
                    <td>{getAnswerBadge(userAnswer, question.correct_option)}</td>
                    <td>
                      <strong>{question.correct_option}</strong>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </Table>

          <div className="text-end">
            <Button variant="primary" onClick={() => navigate("/dashboard")}>
              🔙 Back to Dashboard
            </Button>
          </div>
        </>
      )}
    </Container>
  );
};

export default QuizPerformance;
