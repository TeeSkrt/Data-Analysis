import React from 'react';
import './CSS/HomePage.css';

function HomePage() {
    return (
        <div className="home-page">
            {/* Navbar */}
            <nav className="navbar">
                <div className="logo">
                    <img
                        src={`${process.env.PUBLIC_URL}/logo-bachkhoa.png`}
                        alt="Logo"
                        className="logo-img"
                    />
                    Ecomlytics
                </div>
                <ul className="nav-links">
                    <li><a href="/Home">Home</a></li>
                    <li><a href="/About">About</a></li>
                    <li><a href="/Services">Services</a></li>
                    <li><a href="/Contact">Contact</a></li>
                </ul>
                <div className="hamburger">
                    ☰
                </div>
            </nav>

            {/* Content */}
            <div className="text-content">
                <h1>SALES</h1>
                <h1>DATA ANALYSIS</h1>
                <h2>ON E-COMMERCE</h2>
                <h2>PLATFORM</h2>
            </div>

            {/* Logo and Tech Effect */}
            <div className="logo-main-container">
                <img
                    src={`${process.env.PUBLIC_URL}/logo-main.png`}
                    alt="Sales Data Analysis Logo"
                    className="logo-main"
                />
                <div className="tech-effect"></div>
            </div>
        </div>
    );
}

export default HomePage;
