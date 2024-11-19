// Components/HomePage.js
import React, { useState } from 'react';
import './CSS/HomePage.css';
import About from './About';
import Contact from './Contact';
import Services from './Services';
import Navbar from './Navbar';

function HomePage({ setVisibleSection }) {
    const [visibleSection, setVisibleSectionState] = useState('Home');

    const handleNavigate = (section) => {
        setVisibleSectionState(section);
        setVisibleSection(section);
    };

    return (
        <div className="home-page">
            {/* Navbar */}
            <Navbar onNavigate={handleNavigate} />

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
        </div>
    );
}

export default HomePage;
