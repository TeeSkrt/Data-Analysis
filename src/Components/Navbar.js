// Components/Navbar.js
import React from 'react';
import './CSS/Navbar.css';

function Navbar({ onNavigate }) {
    return (
        <nav className="navbar">
            <div className="logo" onClick={() => onNavigate('Home')} style={{ cursor: 'pointer' }}>
                <img
                    src={`${process.env.PUBLIC_URL}/logo-bachkhoa.png`}
                    alt="Logo"
                    className="logo-img"
                />
                Ecomlytics
            </div>
            <ul className="nav-links">
                <li><span onClick={() => onNavigate('About')} className="nav-item">About</span></li>
                <li><span onClick={() => onNavigate('Services')} className="nav-item">Services</span></li>
                <li><span onClick={() => onNavigate('Contact')} className="nav-item">Contact</span></li>
            </ul>
            <div className="hamburger">☰</div>
        </nav>
    );
}

export default Navbar;
