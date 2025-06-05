import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";
import AdminDashboard from "./pages/AdminDashboard";
import AddChapter from "./pages/AddChapter";
import AddQuiz from "./pages/AddQuiz";
import AddSubject from "./pages/AddSubject";
import AdminAbout from "./pages/AdminAbout";
import AdminAnalytics from "./pages/AdminAnalytics";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AdminLayout />}>
          <Route index element={<AdminDashboard />} />
          <Route path="add-chapter" element={<AddChapter />} />
          <Route path="add-quiz" element={<AddQuiz />} />
          <Route path="add-subject" element={<AddSubject />} />
          <Route path="admin-about" element={<AdminAbout />} />
          <Route path="admin-analytics" element={<AdminAnalytics />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;


