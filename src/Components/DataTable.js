import React, { useState, useEffect } from 'react';
import './CSS/DataTable.css';

function DataTable() {
    const [tableData, setTableData] = useState([]);
    const [loading, setLoading] = useState(true);

    // Lấy dữ liệu từ API giả lập
    useEffect(() => {
        // Thay đổi URL này thành API cloud của bạn
        fetch('https://api.example.com/products')
            .then(response => response.json())
            .then(data => {
                setTableData(data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="table-container">
            <h1>Data Table</h1>
            <table className="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Product Name</th>
                        <th>Sales</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {tableData.map(item => (
                        <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.name}</td>
                            <td>{item.sales}</td>
                            <td>{item.date}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default DataTable;
