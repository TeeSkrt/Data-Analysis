import React, { useState, useEffect } from "react";
import "./CSS/DataTable.css";

function DataTable() {
    const [tableData, setTableData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

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
    }, [currentPage]);

    const filteredData = tableData.filter(
        (item) =>
            item.product.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.avg_rating.toString().includes(searchQuery) ||
            item.asin.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    const generatePageNumbers = () => {
        const maxPagesToShow = 5;
        let pages = [];
        if (totalPages <= maxPagesToShow) {
            for (let i = 1; i <= totalPages; i++) {
                pages.push(i);
            }
        } else {
            if (currentPage <= 3) {
                pages = [1, 2, 3, 4, 5, "...", totalPages];
            } else if (currentPage >= totalPages - 2) {
                pages = [1, "...", totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages];
            } else {
                pages = [1, "...", currentPage - 2, currentPage - 1, currentPage, currentPage + 1, currentPage + 2, "...", totalPages];
            }
        }
        return pages;
    };

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="data-table-page">
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
                                        style={{ width: "50px", height: "50px" }}
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
                {filteredData.length === 0 && <div className="no-results">No matching results found.</div>}

                <div className="pagination">
                    {generatePageNumbers().map((page, index) => (
                        <button
                            key={index}
                            onClick={() => {
                                if (page !== "...") {
                                    handlePageChange(page);
                                }
                            }}
                            className={currentPage === page ? "active" : ""}
                            disabled={page === "..."}
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
