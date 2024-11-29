import React, { useState } from 'react';
import './CSS/HomePage.css';
import About from './About';
import Contact from './Contact';
import Services from './Services';
import Navbar from './Navbar';
import logo from './CSS/logo-main.png'; // Đường dẫn đến logo-main.png


function HomePage() {
    const [visibleSection, setVisibleSection] = useState('Home');

    const handleNavigate = (section) => {
        setVisibleSection(section);
    };

    return (
        <div className="home-page">
            {/* Navbar */}
            <Navbar onNavigate={handleNavigate} />

            {/* Nội dung hiển thị */}
            {visibleSection === 'Home' && (
                <div className="text-content">
                    <div>
                        <h1>SALES</h1>
                        <h2>DATA ANALYSIS</h2>
                        <h2>ON E-COMMERCE</h2>
                        <h2>PLATFORM</h2>
                    </div>
                    <img src={logo} alt="Logo" className="logo-main" />
                </div>
            )}

            {visibleSection === 'About' && <About />}
            {visibleSection === 'Services' && <Services />}
            {visibleSection === 'Contact' && <Contact />}

        </div>
    );
}

export default HomePage;
