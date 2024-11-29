import React, { useState } from 'react';
import './CSS/Navbar.css';

function Navbar({ onNavigate }) {
    const [isMenuOpen, setIsMenuOpen] = useState(false); // Trạng thái để quản lý mở/đóng menu

    // Hàm để toggle trạng thái menu
    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    return (
        <nav className="navbar">
            {/* Logo phần đầu */}
            <div className="logo" onClick={() => onNavigate('Home')} style={{ cursor: 'pointer' }}>
                <img
                    src={`${process.env.PUBLIC_URL}/logo-bachkhoa.png`}
                    alt="Logo"
                    className="logo-img"
                />
                Ecomlytics
            </div>

            {/* Các mục điều hướng */}
            <ul className={`nav-links ${isMenuOpen ? 'active' : ''}`}>
                <li><span onClick={() => onNavigate('About')} className="nav-item">About</span></li>
                <li><span onClick={() => onNavigate('Services')} className="nav-item">Services</span></li>
                <li><span onClick={() => onNavigate('Contact')} className="nav-item">Contact</span></li>

            </ul>

            {/* Hamburger Menu cho thiết bị di động */}
            <div className="hamburger" onClick={toggleMenu}>
                ☰
            </div>
        </nav>
    );
}

export default Navbar;
