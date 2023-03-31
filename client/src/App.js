import logo from './logo.svg';
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import './App.css';
import { TestPage } from './pages/TestPage';
import { HomePage } from './pages/HomePage';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<HomePage />}/>
        <Route path="/test" element={<TestPage />}/>
      </Routes>
    </Router>
  );
}
