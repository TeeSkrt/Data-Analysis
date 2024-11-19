import React, { useState, useEffect } from 'react';
import './CSS/DataTable.css';

function DataTable() {
    const [tableData, setTableData] = useState([]);
    const [loading, setLoading] = useState(true);

    // Lấy dữ liệu từ API giả lập (JSONPlaceholder)
    useEffect(() => {
        fetch('https://jsonplaceholder.typicode.com/posts')
            .then(response => response.json())
            .then(data => {
                setTableData(data); // Lưu trữ dữ liệu vào state
                setLoading(false); // Đặt loading thành false khi đã có dữ liệu
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                setLoading(false); // Đặt loading thành false nếu có lỗi
            });
    }, []);

    // Ngừng cuộn trang khi chuột ở trong bảng
    const handleWheel = (e) => {
        // Ngừng cuộn trang khi con trỏ chuột trong vùng của bảng
        e.preventDefault();
        e.stopPropagation();

        // Cuộn trong bảng
        if (e.deltaY !== 0) {
            e.target.scrollTop += e.deltaY; // Di chuyển bảng khi cuộn
        }
    };

    // Xử lý sự kiện khi chuột rời khỏi bảng để có thể cuộn trang lại
    const handleMouseLeave = () => {
        window.addEventListener('wheel', handlePageScroll, { passive: false });
    };

    // Phục hồi cuộn trang mặc định khi chuột không còn trong bảng
    const handlePageScroll = (e) => {
        if (window.scrollY === 0) {
            e.preventDefault(); // Ngừng cuộn khi ở đầu trang
        }
    };

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="table-container" onWheel={handleWheel} onMouseLeave={handleMouseLeave}>
            <h1>Data Table</h1>
            <table className="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Body</th>
                    </tr>
                </thead>
                <tbody>
                    {tableData.map(item => (
                        <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.title}</td>
                            <td>{item.body}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default DataTable;
