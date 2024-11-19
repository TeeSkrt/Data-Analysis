import React, { useState } from 'react';
import './CSS/HomePage.css';
import About from './About';
import Contact from './Contact';
import Services from './Services';

function HomePage({ setVisibleSection }) {
    const [visibleSection, setVisibleSectionState] = useState('Home'); // Local state for section visibility

    return (
        <div className="home-page">
            {/* Navbar */}
            <nav className="navbar">
                <div className="logo" onClick={() => {
                    setVisibleSectionState('Home');
                    setVisibleSection('Home');
                }} style={{ cursor: 'pointer' }}>
                    <img
                        src={`${process.env.PUBLIC_URL}/logo-bachkhoa.png`}
                        alt="Logo"
                        className="logo-img"
                    />
                    Ecomlytics
                </div>
                <ul className="nav-links">
                    <li><span onClick={() => {
                        setVisibleSectionState('About');
                        setVisibleSection('About');
                    }} className="nav-item">About</span></li>
                    <li><span onClick={() => {
                        setVisibleSectionState('Services');
                        setVisibleSection('Services');
                    }} className="nav-item">Services</span></li>
                    <li><span onClick={() => {
                        setVisibleSectionState('Contact');
                        setVisibleSection('Contact');
                    }} className="nav-item">Contact</span></li>
                </ul>
                <div className="hamburger">☰</div>
            </nav>

            {/* Nội dung hiển thị */}
            {visibleSection === 'Home' && (
                <div className="text-content">
                    <h1>SALES</h1>
                    <h1>DATA ANALYSIS</h1>
                    <h2>ON E-COMMERCE</h2>
                    <h2>PLATFORM</h2>
                </div>
            )}

            {visibleSection === 'About' && <About />}
            {visibleSection === 'Services' && <Services />}
            {visibleSection === 'Contact' && <Contact />}

            {/* Logo và hiệu ứng công nghệ */}
            {visibleSection === 'Home' && (
                <div className="logo-main-container">
                    <img
                        src={`${process.env.PUBLIC_URL}/logo-main.png`}
                        alt="Sales Data Analysis Logo"
                        className="logo-main"
                    />
                    <div className="tech-effect"></div>
                </div>
            )}
        </div>
    );
}

export default HomePage;
