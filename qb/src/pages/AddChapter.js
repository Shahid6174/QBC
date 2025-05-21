import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const AddChapter = () => {
  const navigate = useNavigate();
  const { subjectId } = useParams();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

 
  const subject = {
    id: subjectId,
    name: "Sample Subject",
    description: "This is a short description of the subject."
  };

  const handleSubmit = (e) => {
    e.preventDefault();

   
    console.log("Chapter Data Submitted:", {
      subjectId,
      name,
      description,
    });

   
  };

  return (
    <div>
      <h2>Add Chapter to {subject.name}</h2>
      <p className="text-muted">{subject.description}</p>
      <hr />

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="name" className="form-label">Chapter Name</label>
          <input
            type="text"
            className="form-control"
            id="name"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        <div className="mb-3">
          <label htmlFor="description" className="form-label">Description</label>
          <textarea
            className="form-control"
            id="description"
            rows="3"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        <button type="submit" className="btn btn-success">Add Chapter</button>
        <button
          type="button"
          className="btn btn-secondary ms-2"
          onClick={() => navigate(`/view-chapters/${subject.id}`)}
        >
          Cancel
        </button>
      </form>
    </div>
  );
};

export default AddChapter;
