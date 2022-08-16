import "./App.css";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SoloGameHub from "./pages/SoloGame/SoloGameHub";
import SoloGame from "./pages/SoloGame/SoloGame";
import MultiplayerGame from "./pages/MultiplayerGame/MultiplayerGame";
import MultiplayerGameHub from "./pages/MultiplayerGame/MultiplayerGameHub";
import ProblemEditor from "./pages/ProblemsApi/ProblemEditor";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/allenamento" element={<SoloGameHub />} />
      <Route path="/allenamento/sessione" element={<SoloGame />} />
      <Route path="/sfida" element={<MultiplayerGameHub />} />
      <Route path="/sfida/sessione" element={<MultiplayerGame />} />
      <Route path="/problema/editor" element={<ProblemEditor />} />
    </Routes>
  );
}

export default App;
