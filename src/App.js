import React, { useRef, useState } from 'react';
import './App.css';
import HomePage from './Components/HomePage';
import DataTable from './Components/DataTable';
import Barchart from './Charts/Barchart';
import About from './Components/About';
import Contact from './Components/Contact';
import Services from './Components/Services';
import Navbar from './Components/Navbar';

function App() {
  const sections = useRef([]); // Danh sách các section
  const [visibleSection, setVisibleSection] = useState('Home'); // Section hiện tại
  const [navbarBgColor, setNavbarBgColor] = useState(''); // Màu nền của navbar

  // Danh sách section cho phép cuộn
  const scrollableSections = ['Home', 'DataTable', 'Barchart'];

  // Hàm xử lý cuộn trang
  const handleScroll = (e) => {
    const tableContainerElement = document.querySelector(".table-container");

    if (tableContainerElement && tableContainerElement.contains(e.target)) {
      e.stopPropagation();
      return; // Ngừng cuộn trang khi chuột ở trong bảng dữ liệu
    }

    if (!scrollableSections.includes(visibleSection)) return;

    const delta = e.deltaY > 0 ? 1 : -1;
    const currentIndex = scrollableSections.indexOf(visibleSection);
    const nextIndex = Math.max(0, Math.min(scrollableSections.length - 1, currentIndex + delta));
    const nextSection = scrollableSections[nextIndex];

    if (nextSection === visibleSection) return;

    const targetElement = sections.current.find((el) => el?.id === nextSection);
    if (targetElement) {
      setVisibleSection(nextSection);
      targetElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Hàm điều hướng từ Navbar
  const handleNavigate = (section) => {
    const targetElement = sections.current.find((el) => el?.id === section);
    if (targetElement) {
      setVisibleSection(section);
      targetElement.scrollIntoView({ behavior: 'smooth' });

      // Thay đổi màu nền navbar khi người dùng chọn các mục
      if (section === 'About' || section === 'Services' || section === 'Contact') {
        setNavbarBgColor('#003c64'); // Đổi màu nền thành đen khi chọn About, Services, hoặc Contact
      } else {
        setNavbarBgColor(''); // Giữ màu nền mặc định nếu không phải các mục trên
      }
    }
  };

  return (
    <div className="slides-container" onWheel={handleScroll}>
      {/* Navbar */}
      <Navbar onNavigate={handleNavigate} navbarBgColor={navbarBgColor} />

      {/* Sections */}
      <section
        id="Home"
        ref={(el) => (sections.current[0] = el)}
        className={`slide ${visibleSection === 'Home' ? 'slide-active' : ''}`}
      >
        <HomePage />
      </section>

      <section
        id="About"
        ref={(el) => (sections.current[1] = el)}
        className={`slide ${visibleSection === 'About' ? 'slide-active' : ''}`}
      >
        <About />
      </section>

      <section
        id="Services"
        ref={(el) => (sections.current[2] = el)}
        className={`slide ${visibleSection === 'Services' ? 'slide-active' : ''}`}
      >
        <Services />
      </section>

      <section
        id="Contact"
        ref={(el) => (sections.current[3] = el)}
        className={`slide ${visibleSection === 'Contact' ? 'slide-active' : ''}`}
      >
        <Contact />
      </section>

      <section
        id="DataTable"
        ref={(el) => (sections.current[4] = el)}
        className={`slide ${visibleSection === 'DataTable' ? 'slide-active' : ''}`}
      >
        <DataTable />
      </section>

      <section
        id="Barchart"
        ref={(el) => (sections.current[5] = el)}
        className={`slide ${visibleSection === 'Barchart' ? 'slide-active' : ''}`}
      >
        <Barchart />
      </section>
    </div>
  );
}

export default App;
