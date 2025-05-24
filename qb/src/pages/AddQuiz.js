import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";

const AddQuiz = () => {
  const { subjectId, chapterId } = useParams(); 
  const navigate = useNavigate();

  const [timeDuration, setTimeDuration] = useState("");
  const [remarks, setRemarks] = useState("");

  const chapterName = "Sample Chapter"; 

  const handleSubmit = (e) => {
    e.preventDefault();

    
    console.log("Submitted:", {
      timeDuration,
      remarks,
    });

    
  };

  return (
    <div>
      <h2 className="mb-4">
        Add Quiz for <strong>{chapterName}</strong>
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="time_duration">Time Duration (in minutes)</label>
          <input
            type="number"
            className="form-control"
            required
            id="time_duration"
            value={timeDuration}
            onChange={(e) => setTimeDuration(e.target.value)}
          />
        </div>

        <div className="form-group mt-3">
          <label htmlFor="remarks">Remarks (Optional)</label>
          <input
            type="text"
            className="form-control"
            id="remarks"
            value={remarks}
            onChange={(e) => setRemarks(e.target.value)}
          />
        </div>

        <button type="submit" className="btn btn-success mt-3">
          Add Quiz
        </button>
        <button
          type="button"
          className="btn btn-secondary mt-3 ms-2"
          onClick={() =>
            navigate(`/view-chapters/${subjectId}/${chapterId}`)
          }
        >
          Cancel
        </button>
      </form>
    </div>
  );
};

export default AddQuiz;
