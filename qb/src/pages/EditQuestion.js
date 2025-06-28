import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
// For Bootstrap components
import { Container, Form, Button } from 'react-bootstrap';
// For Chart.js
import 'chart.js/auto';


const EditQuestion = () => {
  const { questionId } = useParams();
  const navigate = useNavigate();

  const [questionData, setQuestionData] = useState({
    question_text: "",
    option_a: "",
    option_b: "",
    option_c: "",
    option_d: "",
    correct_option: "",
  });

  useEffect(() => {
    fetch(`/api/questions/${questionId}`)
      .then(res => res.json())
      .then(data => setQuestionData(data))
      .catch(err => console.error("Failed to fetch question:", err));
  }, [questionId]);

  const handleChange = (e) => {
    setQuestionData({ ...questionData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch(`/api/questions/${questionId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(questionData),
    })
      .then((res) => {
        if (res.ok) {
          navigate(`/view-quizzes/${questionData.chapter_id}`);
        } else {
          console.error("Update failed");
        }
      })
      .catch((err) => console.error("Error updating question:", err));
  };

  return (
    <Container className="mt-4">
      <h2>Edit Question</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Question:</Form.Label>
          <Form.Control
            type="text"
            name="question_text"
            value={questionData.question_text}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Option A:</Form.Label>
          <Form.Control
            type="text"
            name="option_a"
            value={questionData.option_a}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Option B:</Form.Label>
          <Form.Control
            type="text"
            name="option_b"
            value={questionData.option_b}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Option C:</Form.Label>
          <Form.Control
            type="text"
            name="option_c"
            value={questionData.option_c}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Option D:</Form.Label>
          <Form.Control
            type="text"
            name="option_d"
            value={questionData.option_d}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Correct Option (A/B/C/D):</Form.Label>
          <Form.Control
            type="text"
            name="correct_option"
            value={questionData.correct_option}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Button variant="primary" type="submit">Update Question</Button>{" "}
        <Button variant="secondary" onClick={() => navigate(`/view-quizzes/${questionData.chapter_id}`)}>
          Cancel
        </Button>
      </Form>
    </Container>
  );
};

export default EditQuestion;
