// Components/DataTable.js
import React, { useState, useEffect } from 'react';
import './CSS/DataTable.css';
import Navbar from './Navbar';

function DataTable({ setVisibleSection }) {
    const [tableData, setTableData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');

    // Lấy dữ liệu từ API giả lập
    useEffect(() => {
        fetch('https://jsonplaceholder.typicode.com/posts')
            .then((response) => response.json())
            .then((data) => {
                setTableData(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                setLoading(false);
            });
    }, []);

    const filteredData = tableData.filter(
        (item) =>
            item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.body.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.id.toString().includes(searchQuery)
    );

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    const handleNavigate = (section) => {
        setVisibleSection(section);
    };

    return (
        <div className="data-table-page">
            {/* Navbar */}
            <Navbar onNavigate={handleNavigate} />

            {/* Nội dung bảng */}
            <div className="table-container">
                <h1>Data Table</h1>
                <input
                    type="text"
                    className="search-bar"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <table className="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Body</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredData.map((item) => (
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.title}</td>
                                <td>{item.body}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {filteredData.length === 0 && (
                    <div className="no-results">No matching results found.</div>
                )}
            </div>
        </div>
    );
}

export default DataTable;
