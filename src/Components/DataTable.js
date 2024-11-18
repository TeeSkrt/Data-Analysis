import React from 'react';

function DataTable() {
    const tableData = [
        { id: 1, name: "Product 1", sales: 1200, date: "2024-10-10" },
        { id: 2, name: "Product 2", sales: 1500, date: "2024-10-12" },
        { id: 3, name: "Product 3", sales: 900, date: "2024-10-15" },
        { id: 4, name: "Product 4", sales: 300, date: "2024-10-18" },
        { id: 5, name: "Product 5", sales: 2500, date: "2024-10-20" },
    ];

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
