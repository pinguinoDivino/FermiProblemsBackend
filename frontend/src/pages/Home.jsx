import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div>
      <h1>Benvenuti</h1>
      <Link to="/allenamento">Allenamento</Link>
      <br />
      <Link to="/sfida">Sfida un avversario!</Link>
      <br />
      <Link to="/problema/editor">Aggiungi un problema!</Link>
    </div>
  );
};

export default Home;
