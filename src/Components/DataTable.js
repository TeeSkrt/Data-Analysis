import React, { useState, useEffect } from "react";
import "./CSS/DataTable.css";

function DataTable() {
    const [tableData, setTableData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [sortField, setSortField] = useState(""); // Không gán giá trị mặc định là "price"
    const [sortOrder, setSortOrder] = useState("desc"); // Thứ tự sắp xếp mặc định
    const [apiUrl, setApiUrl] = useState(`https://bedata.azurewebsites.net/api/getdata/?page=1`);

    // Fetch dữ liệu từ API mỗi khi URL thay đổi
    useEffect(() => {
        setLoading(true);
        fetch(apiUrl)
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
    }, [apiUrl]);

    // Hàm xử lý sắp xếp theo trường dữ liệu bất kỳ
    const handleSort = (field) => {
        const newOrder = sortOrder === "desc" ? "asc" : "desc"; // Toggle thứ tự
        setSortField(field);
        setSortOrder(newOrder);

        const searchParam = searchQuery ? `&search=${searchQuery}` : "";
        const baseApiUrl = apiUrl.includes("/sort/")
            ? "https://bedata.azurewebsites.net/api/getdata/sort/"
            : "https://bedata.azurewebsites.net/api/getdata/";

        setApiUrl(`${baseApiUrl}?page=1${searchParam}&sort_field=${field}&sort_order=${newOrder}`);
    };

    // Hàm xử lý sắp xếp theo Best Seller (dùng nút)
    const handleSortByBestSeller = () => {
        setSortField("predicted_best_seller");
        setSortOrder("desc"); // Best Seller chỉ có giảm dần
        const searchParam = searchQuery ? `&search=${searchQuery}` : "";
        setApiUrl(`https://bedata.azurewebsites.net/api/getdata/sort/?page=1${searchParam}&sort_field=predicted_best_seller&sort_order=desc`);
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
        const searchParam = searchQuery ? `&search=${searchQuery}` : "";

        // Nếu không muốn sắp xếp mặc định, reset sortField và sortOrder
        if (!sortField) {
            setSortField(""); // Reset lại trường sắp xếp
            setSortOrder(""); // Reset lại thứ tự mặc định
        }

        const baseApiUrl = apiUrl.includes("/sort/")
            ? "https://bedata.azurewebsites.net/api/getdata/sort/"
            : "https://bedata.azurewebsites.net/api/getdata/";

        setApiUrl(`${baseApiUrl}?page=${page}${searchParam}${sortField ? `&sort_field=${sortField}&sort_order=${sortOrder}` : ""}`);
    };

    const resetToDefaultAPI = () => {
        setSearchQuery("");
        setCurrentPage(1);
        setSortField(""); // Đặt lại `sortField` thành chuỗi rỗng
        setSortOrder("desc");
        setApiUrl(`https://bedata.azurewebsites.net/api/getdata/?page=1`);
    };

    const handleSearchChange = (e) => {
        setSearchQuery(e.target.value);
        setCurrentPage(1);
        const searchParam = e.target.value ? `&search=${e.target.value}` : "";
        const baseApiUrl = apiUrl.includes("/sort/")
            ? "https://bedata.azurewebsites.net/api/getdata/sort/"
            : "https://bedata.azurewebsites.net/api/getdata/";

        setApiUrl(`${baseApiUrl}?page=1${searchParam}${sortField ? `&sort_field=${sortField}&sort_order=${sortOrder}` : ""}`);
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
                    onChange={handleSearchChange}
                />
                <button className="sort-button" onClick={handleSortByBestSeller}>
                    Sort by Predicted Best Seller
                </button>
                <button className="reset-button" onClick={resetToDefaultAPI}>
                    Reset
                </button>
            </div>

            <div className="table-container">
                <h1>Data Table</h1>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Image</th>
                            <th>ASIN</th>
                            <th>Product</th>
                            <th
                                onClick={() => handleSort("price")}
                                style={{ cursor: "pointer" }}
                            >
                                Price {sortField === "price" && (sortOrder === "desc" ? "↓" : "↑")}
                            </th>
                            <th>Rating</th>
                            <th>Review</th>
                            <th
                                onClick={() => handleSort("amount")}
                                style={{ cursor: "pointer" }}
                            >
                                Amount {sortField === "amount" && (sortOrder === "desc" ? "↓" : "↑")}
                            </th>
                            <th>Predicted Best Seller</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tableData.map((item) => (
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
                {tableData.length === 0 && <div className="no-results">No matching results found.</div>}

                <div className="pagination">
                    {generatePageNumbers().map((page, index) => (
                        <button
                            key={index}
                            onClick={() => handlePageChange(page)}
                            className={currentPage === page ? "active" : ""}
                            disabled={page === "..."} >
                            {page}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default DataTable;
