import React, { useState, useEffect } from 'react';
import './CSS/DataTable.css';
import Navbar from './Navbar';

function DataTable({ setVisibleSection }) {
    const [tableData, setTableData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    // Fetch data from API
    useEffect(() => {
        fetch(`https://bedata.azurewebsites.net/api/getdata/?format=json&page=${currentPage}`)
            .then((response) => response.json())
            .then((data) => {
                setTableData(data.data);
                setTotalPages(data.total_pages);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                setLoading(false);
            });
    }, [currentPage]);  // Gọi lại API khi currentPage thay đổi


    // Filter table data based on search query
    const filteredData = tableData.filter(
        (item) =>
            item.product.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.avg_rating.toString().includes(searchQuery) ||
            item.asin.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Navigate to different sections
    const handleNavigate = (section) => {
        setVisibleSection(section);
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    // Generate paginated page numbers
    const generatePageNumbers = () => {
        const maxPagesToShow = 5;  // Số trang tối đa muốn hiển thị
        let pages = [];

        if (totalPages <= maxPagesToShow) {
            // Nếu tổng số trang ít hơn hoặc bằng maxPagesToShow, hiển thị tất cả các trang
            for (let i = 1; i <= totalPages; i++) {
                pages.push(i);
            }
        } else {
            // Nếu số trang lớn hơn maxPagesToShow
            if (currentPage <= 3) {
                // Nếu trang hiện tại ở đầu (trang 1, 2, 3)
                pages = [1, 2, 3, 4, 5, '...', totalPages];
            } else if (currentPage >= totalPages - 2) {
                // Nếu trang hiện tại ở gần cuối
                pages = [1, '...', totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages];
            } else {
                // Nếu trang hiện tại ở giữa
                pages = [
                    1, '...',
                    currentPage - 2, currentPage - 1, currentPage, currentPage + 1, currentPage + 2, '...',
                    totalPages
                ];
            }
        }

        return pages;
    };



    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="data-table-page">
            <Navbar onNavigate={handleNavigate} />

            <div className="search-bar-container">
                <input
                    type="text"
                    className="search-bar"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </div>

            <div className="table-container">
                <h1>Data Table</h1>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Image</th>
                            <th>ASIN</th>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Rating</th>
                            <th>Review</th>
                            <th>Amount</th>
                            <th>Predicted Best Seller</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredData.map((item) => (
                            <tr key={item.asin}>
                                <td>
                                    <img
                                        src={item.image}
                                        alt={item.product}
                                        className="product-image"
                                        style={{ width: '50px', height: '50px' }}
                                    />
                                </td>
                                <td>{item.asin}</td>
                                <td>{item.product}</td>
                                <td>{item.price}</td>
                                <td>{item.avg_rating}</td>
                                <td>{item.review}</td>
                                <td>{item.amount}</td>
                                <td>{item.predicted_best_seller ? "Yes" : "No"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {filteredData.length === 0 && (
                    <div className="no-results">No matching results found.</div>
                )}

                <div className="pagination">
                    {generatePageNumbers().map((page, index) => (
                        <button
                            key={index}
                            onClick={() => {
                                if (page !== '...') {
                                    handlePageChange(page);
                                }
                            }}
                            className={currentPage === page ? "active" : ""}
                            disabled={page === '...'}
                        >
                            {page}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default DataTable;
