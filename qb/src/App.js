import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";

import AddChapter from "./pages/AddChapter";
import AddQuiz from "./pages/AddQuiz";
import AdminAbout from "./pages/AdminAbout";
import AdminAnalytics from "./pages/AdminAnalytics";
import AdminDashboard from "./pages/AdminDashboard";
import EditQuestion from "./pages/EditQuestion";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AdminLayout />}>
          <Route index element={<AdminDashboard />} />
          <Route path="subject/:subjectId/add-quiz/:chapterId" element={<AddQuiz />} />
          <Route path="subject/:subjectId/add-chapter" element={<AddChapter />} />
          <Route path="question/edit/:id" element={<EditQuestion />} />
          <Route path="about" element={<AdminAbout />} />
          <Route path="analytics" element={<AdminAnalytics />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;


