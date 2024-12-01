import React from 'react';
import './CSS/HomePage.css';
import logo from './CSS/logo-main.png'; // Đường dẫn đến logo-main.png

function HomePage() {
    return (
        <div className="home-page">
            <div className="text-content">
                <div>
                    <h1>SALES</h1>
                    <h2>DATA ANALYSIS</h2>
                    <h2>ON E-COMMERCE</h2>
                    <h2>PLATFORM</h2>
                </div>
                <img src={logo} alt="Logo" className="logo-main" />
            </div>
        </div>
    );
}

export default HomePage;
