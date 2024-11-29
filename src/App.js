import React, { useRef, useState } from 'react';
import './App.css';
import HomePage from './Components/HomePage';
import DataTable from './Components/DataTable';
import Barchart from './Charts/Barchart';
import Navbar from './Components/Navbar';

function App() {
  const sections = useRef([]);
  const isScrolling = useRef(false);
  const [visibleSection, setVisibleSection] = useState('Home'); // Quản lý section hiện tại

  // Hàm xử lý khi người dùng cuộn trang
  const handleScroll = (e) => {
    // Kiểm tra nếu con trỏ chuột đang nằm trong bảng (DataTable)
    const isInTable = e.target.closest('.table-container');
    if (isInTable) {
      // Nếu đang trong bảng, không cuộn trang chính
      return;
    }

    if (isScrolling.current) return;

    isScrolling.current = true;

    // Xác định chiều hướng cuộn: xuống (deltaY > 0) hoặc lên (deltaY < 0)
    const delta = e.deltaY > 0 ? 1 : -1;

    // Tìm index của section hiện tại đang hiển thị
    const currentIndex = sections.current.findIndex((section) => {
      const rect = section.getBoundingClientRect();
      return rect.top < window.innerHeight / 2 && rect.top > -window.innerHeight / 2;
    });

    // Tính toán index của section kế tiếp
    const nextIndex = Math.max(0, Math.min(sections.current.length - 1, currentIndex + delta));

    // Chỉ thực hiện cuộn nếu section hiện tại khác với section tiếp theo
    if (currentIndex !== nextIndex) {
      setVisibleSection(sections.current[nextIndex].id);  // Cập nhật section hiện tại
      sections.current[nextIndex].scrollIntoView({ behavior: 'smooth' });  // Cuộn đến section mới
    }

    // Chờ một khoảng thời gian trước khi có thể cuộn lại
    setTimeout(() => {
      isScrolling.current = false;
    }, 800);  // Điều chỉnh thời gian này để đảm bảo hiệu ứng cuộn đủ mượt mà
  };

  return (
    <div className="slides-container" onWheel={handleScroll}>
      {/* Navbar */}
      <Navbar onNavigate={setVisibleSection} />

      {/* Các sections */}
      <section
        id="Home"
        ref={(el) => (sections.current[0] = el)}
        className={`slide ${visibleSection === 'Home' ? 'slide-active' : ''}`}
      >
        <HomePage setVisibleSection={setVisibleSection} />
      </section>

      <section
        id="DataTable"
        ref={(el) => (sections.current[1] = el)}
        className={`slide ${visibleSection === 'DataTable' ? 'slide-active' : ''}`}
      >
        <DataTable setVisibleSection={setVisibleSection} />
      </section>

      <section
        id="Barchart"
        ref={(el) => (sections.current[2] = el)}
        className={`slide ${visibleSection === 'Barchart' ? 'slide-active' : ''}`}
      >
        <Barchart setVisibleSection={setVisibleSection} />
      </section>
    </div>
  );
}

export default App;
