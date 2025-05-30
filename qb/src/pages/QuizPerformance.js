import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Container, Table, Button } from "react-bootstrap";

const QuizPerformance = () => {
  const { quizAttemptId } = useParams();
  const navigate = useNavigate();

  const [score, setScore] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [userAnswers, setUserAnswers] = useState({});

  useEffect(() => {
    fetch(`/api/quiz-result/${quizAttemptId}`)
      .then((res) => res.json())
      .then((data) => {
        setScore(data.score);
        setQuestions(data.questions);
        setUserAnswers(data.user_answers);
      })
      .catch((err) => console.error("Error fetching quiz result:", err));
  }, [quizAttemptId]);

  return (
    <Container className="mt-4">
      <h2>Quiz Performance</h2>
      {score && <p><strong>Score:</strong> {score.total_score}</p>}

      <Table bordered>
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
            const isCorrect = userAnswer === question.correct_option;

            return (
              <tr key={question.id}>
                <td>{question.question_text}</td>
                <td className={isCorrect ? "text-success" : "text-danger"}>
                  {userAnswer}
                </td>
                <td><strong>{question.correct_option}</strong></td>
              </tr>
            );
          })}
        </tbody>
      </Table>

      <Button onClick={() => navigate("/dashboard")}>Back to Dashboard</Button>
    </Container>
  );
};

export default QuizPerformance;
