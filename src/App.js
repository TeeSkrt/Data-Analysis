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
  const [isInsideDataTable, setIsInsideDataTable] = useState(false); // Kiểm tra con trỏ chuột có ở trong DataTable hay không

  // Danh sách section cho phép cuộn
  const scrollableSections = ['Home', 'DataTable', 'Barchart'];

  // Hàm xử lý cuộn trang
  const handleScroll = (e) => {
    if (isInsideDataTable) {
      // Nếu sự kiện cuộn xảy ra trong bảng, ngừng sự kiện và không thực hiện cuộn trang
      e.stopPropagation();
      return; // Không thực hiện cuộn trang nếu trong bảng
    }

    if (!scrollableSections.includes(visibleSection)) return; // Chỉ xử lý nếu đang ở section cuộn

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
    }
  };

  return (
    <div className="slides-container" onWheel={handleScroll}>
      {/* Navbar */}
      <Navbar onNavigate={handleNavigate} />

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
        style={{ overflow: 'auto', maxHeight: '100vh' }} // Đảm bảo bảng có thể cuộn độc lập
        onMouseEnter={() => setIsInsideDataTable(true)} // Khi chuột vào bảng, không cuộn trang
        onMouseLeave={() => setIsInsideDataTable(false)} // Khi chuột ra khỏi bảng, cho phép cuộn trang
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
