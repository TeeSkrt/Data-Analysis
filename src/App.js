import React, { useRef, useState } from 'react';
import './App.css';
import HomePage from './Components/HomePage';
import About from './Components/About';
import Contact from './Components/Contact';
import Services from './Components/Services';
import DataTable from './Components/DataTable';

function App() {
  const sections = useRef([]); // Mảng tham chiếu cho các phần tử section
  const isScrolling = useRef(false); // Cờ để tránh cuộn không mong muốn khi đang cuộn
  const [activeSection, setActiveSection] = useState(0); // Trạng thái để theo dõi phần đang active

  const handleScroll = (e) => {
    if (isScrolling.current) return; // Bỏ qua nếu đang cuộn
    isScrolling.current = true;

    const delta = e.deltaY > 0 ? 1 : -1; // Xác định hướng cuộn
    const currentIndex = sections.current.findIndex((section) => {
      const rect = section.getBoundingClientRect();
      return rect.top < window.innerHeight / 2 && rect.top > -window.innerHeight / 2; // Điều chỉnh để xác định phần gần viewport
    });

    // Cập nhật phần active khi cuộn
    const nextIndex = Math.max(0, Math.min(sections.current.length - 1, currentIndex + delta));

    if (currentIndex !== nextIndex) {
      setActiveSection(nextIndex); // Cập nhật phần active
      sections.current[nextIndex].scrollIntoView({ behavior: 'smooth' });
    }

    // Đặt lại cờ sau khi cuộn hoàn tất
    setTimeout(() => {
      isScrolling.current = false;
    }, 800); // Thời gian khớp với hiệu ứng smooth
  };

  return (
    <div className="slides-container" onWheel={handleScroll}>
      {/* Home Page Slide */}
      <section
        ref={(el) => (sections.current[0] = el)}
        className={`slide ${activeSection === 0 ? 'slide-active' : ''}`}
      >
        <HomePage />
      </section>

      {/* Data Table Slide */}
      <section
        ref={(el) => (sections.current[1] = el)}
        className={`slide ${activeSection === 1 ? 'slide-active' : ''}`}
      >
        <DataTable />
      </section>

      About Slide
      <section
        ref={(el) => (sections.current[2] = el)}
        className={`slide ${activeSection === 2 ? 'slide-active' : ''}`}
      >
        <About />
      </section>

      {/* Contact Slide */}
      <section
        ref={(el) => (sections.current[3] = el)}
        className={`slide ${activeSection === 3 ? 'slide-active' : ''}`}
      >
        <Contact />
      </section>

      {/* Services Slide */}
      <section
        ref={(el) => (sections.current[4] = el)}
        className={`slide ${activeSection === 4 ? 'slide-active' : ''}`}
      >
        <Services />
      </section>
    </div>
  );
}

export default App;
