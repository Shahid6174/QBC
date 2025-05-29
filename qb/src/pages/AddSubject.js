import { useState } from "react";
import { useNavigate } from "react-router-dom";

const AddSubject = () => {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    qualification: "",
  });

  const [flashMessage, setFlashMessage] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.name || !formData.qualification) {
      setFlashMessage({ type: "danger", text: "Name and Level are required." });
      return;
    }

    console.log("Form submitted:", formData);
    setFlashMessage({ type: "success", text: "Subject added successfully!" });

    
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Add New Subject</h2>

      {flashMessage && (
        <div className={`alert alert-${flashMessage.type}`}>
          {flashMessage.text}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="name" className="form-label">Subject Name</label>
          <input
            type="text"
            className="form-control"
            id="name"
            name="name"
            required
            value={formData.name}
            onChange={handleChange}
          />
        </div>

        <div className="mb-3">
          <label htmlFor="description" className="form-label">Description</label>
          <textarea
            className="form-control"
            id="description"
            name="description"
            rows="3"
            value={formData.description}
            onChange={handleChange}
          />
        </div>

        <div className="mb-3">
          <label htmlFor="qualification" className="form-label">Level</label>
          <select
            className="form-control"
            id="qualification"
            name="qualification"
            required
            value={formData.qualification}
            onChange={handleChange}
          >
            <option value="">Select your Level</option>
            <option value="Foundation">Foundation</option>
            <option value="Diploma in DS">Diploma in DS</option>
            <option value="Diploma in Programming">Diploma in Programming</option>
            <option value="BSc">BSc</option>
            <option value="BS">BS</option>
          </select>
        </div>

        <button type="submit" className="btn btn-success">Add Subject</button>
        <button
          type="button"
          className="btn btn-secondary ms-2"
          onClick={() => navigate("/")}
        >
          Back
        </button>
      </form>
    </div>
  );
};

export default AddSubject;
