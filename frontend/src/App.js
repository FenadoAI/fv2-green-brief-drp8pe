import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import NewsFeed from "./pages/NewsFeed";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<NewsFeed />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
