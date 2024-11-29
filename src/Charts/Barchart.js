import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import './Barchart.css';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function PriceClusterChart() {
    const [chartData, setChartData] = useState({
        labels: [],      // Names of the products
        datasets: [],    // Data for price and quantity
    });

    // Hàm fetch dữ liệu từ trang 1
    const fetchData = async () => {
        try {
            const response = await fetch('https://bedata.azurewebsites.net/api/getdata/?format=json&page=1');
            const data = await response.json();

            // Lấy toàn bộ dữ liệu của trang 1
            const allData = data.data;

            // Sắp xếp sản phẩm theo giá (theo trường 'price') và lấy top 10 sản phẩm có giá cao nhất
            const topProducts = allData
                .sort((a, b) => b.price - a.price)  // Sắp xếp giảm dần theo giá
                .slice(0, 10);  // Lấy top 10 sản phẩm có giá cao nhất

            // Tạo nhãn cho biểu đồ (tên sản phẩm)
            const labels = topProducts.map((item) => item.product);

            // Tạo dữ liệu cho biểu đồ (giá của sản phẩm và số lượng sản phẩm)
            const prices = topProducts.map((item) => item.price);
            const amounts = topProducts.map((item) => item.amount);

            // Cập nhật dữ liệu cho biểu đồ
            setChartData({
                labels,
                datasets: [
                    {
                        label: 'Price ($)',
                        data: prices,
                        backgroundColor: 'rgba(123, 104, 238, 1)',  // Màu sắc cho cột giá
                        borderColor: 'rgba(123, 104, 238, 1)',
                        borderWidth: 1,
                        // Add bar width or group them
                        barPercentage: 0.4,  // Control the width of the bars
                    },
                    {
                        label: 'Amount',
                        data: amounts,
                        backgroundColor: 'rgba(75, 192, 192, 1)',  // Màu sắc cho cột số lượng
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        barPercentage: 0.4,  // Control the width of the bars
                    },
                ],
            });
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        fetchData();  // Gọi hàm fetchData khi component mount
    }, []);  // Chạy 1 lần khi component mount

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    font: {
                        size: 14,
                    },
                    color: 'rgba(0, 0, 0, 0.7)',
                },
            },
            title: {
                display: true,

                text: 'Top 10 Products by Price and Quantity',

            },
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function (value) {
                        return value % 1 === 0 ? `$${value}` : value; // Hiển thị giá trị y là đơn vị tiền tệ (cho cột price)
                    },
                },
            },
        },
    };

    return (
        <div className="chart-container">
            <Bar data={chartData} options={options} />
        </div>
    );
}

export default PriceClusterChart;
