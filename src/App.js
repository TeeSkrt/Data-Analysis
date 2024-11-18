import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import './App.css';
import About from './Components/About';
import Contact from './Components/Contact';
import Services from './Components/Services';


function HomePage() {
  const navigate = useNavigate();
  const [hasNavigated, setHasNavigated] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50 && !hasNavigated) {
        setHasNavigated(true);
        navigate('/data-table'); // Navigate to the data table page
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll); // Cleanup
  }, [navigate, hasNavigated]);

  return (
    <div className="hero">
      <div className="text-container">
        <h1>SALES DATA ANALYSIS</h1>
        <h2>ON E-COMMERCE PLATFORM</h2>
      </div>
      <img src="/logo-main.png" alt="Sales Data Analysis Logo" className="animated-image" />
      <div className="wave"></div> {/* Optional: Animation */}
    </div>
  );
}

function DataTablePage() {
  const tableData = [
    { id: 1, name: "Product 1", sales: 1200, date: "2024-10-10" },
    { id: 2, name: "Product 2", sales: 1500, date: "2024-10-12" },
    { id: 3, name: "Product 3", sales: 900, date: "2024-10-15" },
    { id: 4, name: "Product 4", sales: 300, date: "2024-10-18" },
    { id: 5, name: "Product 5", sales: 2500, date: "2024-10-20" },
  ];

  return (
    <div className="table-container">
      <h1>Data Table</h1>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Product Name</th>
            <th>Sales</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.name}</td>
              <td>{item.sales}</td>
              <td>{item.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function App() {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <Router>
      <div className="app">
        {/* Navbar */}
        <div className="navbar">
          <ul className="menu">
            <li className="menu-item logo">
              <Link to="/">
                <img src="/logobachkhoa.png" alt="Logo" className="logo-img" />
                Ecomlytics
              </Link>
            </li>

            <div className="menu-right">
              <li className="menu-item right"><Link to="/services">Services</Link></li>
              <li className="menu-item right"><Link to="/about">About</Link></li>
              <li className="menu-item right"><Link to="/contact">Contact</Link></li>
            </div>

            <button className="hamburger-btn" onClick={toggleMenu}>
              ☰
            </button>
          </ul>

          <ul className={`dropdown-menu ${menuOpen ? 'active' : ''}`}>
            <li className="dropdown-item"><Link to="/services">Services</Link></li>
            <li className="dropdown-item"><Link to="/about">About</Link></li>
            <li className="dropdown-item"><Link to="/contact">Contact</Link></li>
          </ul>
        </div>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/data-table" element={<DataTablePage />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/services" element={<Services />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
