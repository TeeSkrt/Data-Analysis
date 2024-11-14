import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import About from './Components/About';
import Contact from './Components/Contact';
import Services from './Components/Services';

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const tableData = [
    { id: 1, name: "Product 1", sales: 1200, date: "2024-10-10" },
    { id: 2, name: "Product 2", sales: 1500, date: "2024-10-12" },
    { id: 3, name: "Product 3", sales: 900, date: "2024-10-15" },
    { id: 4, name: "Product 4", sales: 300, date: "2024-10-18" },
    { id: 5, name: "Product 5", sales: 2500, date: "2024-10-20" },
  ];

  const filteredData = tableData.filter(item =>
    item.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Router>
      <div className="app">
        {/* Navbar */}
        <div className="navbar">
          <ul className="menu">
            <li className="menu-item logo">
              <Link to="/">
                <img src="/logo-bachkhoa.png" alt="Logo Trường Đại học Bách Khoa" className="logo-img" />
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
          <Route path="/" element={
            <>
              {/* Hero Section */}
              <div className="hero">
                <h1>SALES DATA ANALYSIS</h1>
                <h2>ON E-COMMERCE PLATFORM</h2>
                <img src="/path-to-your-animated-image.gif" alt="Animated Sales Data Analysis" className="animated-image" />
              </div>

              {/* Searching bar */}
              <div className="search-container">
                <input
                  type="text"
                  className="search-box"
                  value={searchQuery}
                  onChange={handleSearchChange}
                  placeholder="Search for a product..."
                />
                <button className="search-btn">Search</button>
              </div>

              {/* Data Table */}
              <div className="table-container">
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
                    {filteredData.map(item => (
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
            </>
          } />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/services" element={<Services />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
