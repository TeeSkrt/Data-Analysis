import React from 'react';
import './CSS/Navbar.css'; // Đảm bảo đã có file CSS

function Navbar({ onNavigate, navbarBgColor }) {
    return (
        <nav className="navbar" style={{ backgroundColor: navbarBgColor }}>
            <div
                className="logo"
                style={{ cursor: 'pointer' }}
                onClick={() => onNavigate('Home')} // Sự kiện nhấn vào logo
            >
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
        </nav>
    );
}

export default Navbar;
