import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-3 shadow-sm">
      {/* 🔰 Brand Logo */}
      <NavLink className="navbar-brand fw-bold" to="/">
        QBC Admin
      </NavLink>

      {/* 📱 Mobile Toggler */}
      <button
        className="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </button>

      {/* 📁 Collapsible Menu */}
      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav me-auto">
          {/* 🧭 Main Links */}
          <li className="nav-item">
            <NavLink className="nav-link" to="/" end>
              Dashboard
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/add-subject">
              Add Subject
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/add-chapter">
              Add Chapter
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/add-quiz">
              Add Quiz
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/admin-analytics">
              Analytics
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/admin-about">
              About
            </NavLink>
          </li>
        </ul>

        {/* 🔒 Optional Placeholder for future user menu */}
        {/* 
        <ul className="navbar-nav ms-auto">
          <li className="nav-item">
            <NavLink className="nav-link" to="/logout">
              Logout
            </NavLink>
          </li>
        </ul> 
        */}
      </div>
    </nav>
  );
};

export default Navbar;
