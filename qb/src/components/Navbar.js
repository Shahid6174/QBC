import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-3">
      <NavLink className="navbar-brand" to="/">QBC Admin</NavLink>
      <button
        className="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav me-auto">
          <li className="nav-item">
            <NavLink className="nav-link" to="/">Dashboard</NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/add-subject">Add Subject</NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/add-chapter">Add Chapter</NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/add-quiz">Add Quiz</NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/admin-analytics">Analytics</NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/admin-about">About</NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;


