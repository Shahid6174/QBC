import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";
import AdminDashboard from "./pages/AdminDashboard";
import AddQuiz from "./pages/AddQuiz";
import AddChapter from "./pages/AddChapter";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AdminLayout />}>
          <Route index element={<AdminDashboard />} />
          <Route path="subject/:subjectId/add-quiz/:chapterId" element={<AddQuiz />} />
          <Route path="subject/:subjectId/add-chapter" element={<AddChapter />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

