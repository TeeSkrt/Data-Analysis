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
        labels: [],
        datasets: [],
    });
    const [rawData, setRawData] = useState([]); // Lưu dữ liệu gốc từ API
    const [hiddenDatasets, setHiddenDatasets] = useState([]); // Danh sách các dataset bị ẩn

    const fetchData = async () => {
        try {
            const response = await fetch('https://bedata.azurewebsites.net/api/getdata/sort/?page=1&sort_field=price&sort_order=desc');
            const data = await response.json();
            const allData = data.data;

            const topProducts = allData.slice(0, 10);

            setRawData(topProducts); // Lưu trữ dữ liệu gốc
            setChartData({
                labels: topProducts.map((item) => item.product.length > 10 ? item.product.slice(0, 10) + '...' : item.product),
                datasets: [
                    {
                        label: 'Price ($)',
                        data: topProducts.map((item) => item.price),
                        backgroundColor: 'rgba(123, 104, 238, 0.7)',
                        borderColor: 'rgba(123, 104, 238, 1)',
                        borderWidth: 1,
                        barPercentage: 0.35,
                        hoverBackgroundColor: 'rgba(123, 104, 238, 1)',
                    },
                    {
                        label: 'Amount',
                        data: topProducts.map((item) => item.amount),
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        barPercentage: 0.35,
                        hoverBackgroundColor: 'rgba(75, 192, 192, 1)',
                    },
                ],
            });
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleLegendClick = (e, legendItem) => {
        const datasetIndex = legendItem.datasetIndex;
        setHiddenDatasets((prev) =>
            prev.includes(datasetIndex)
                ? prev.filter((index) => index !== datasetIndex) // Hiển thị lại nếu đang bị ẩn
                : [...prev, datasetIndex] // Ẩn nếu đang hiển thị
        );
    };

    useEffect(() => {
        if (hiddenDatasets.includes(0) && !hiddenDatasets.includes(1)) {
            // Nếu Price bị ẩn và Amount hiển thị
            const sortedData = rawData
                .slice()
                .sort((a, b) => b.amount - a.amount); // Sắp xếp theo Amount

            setChartData((prev) => ({
                ...prev,
                labels: sortedData.map((item) =>
                    item.product.length > 10 ? item.product.slice(0, 10) + '...' : item.product
                ), // Cập nhật nhãn theo Amount
                datasets: prev.datasets.map((dataset) => ({
                    ...dataset,
                    data: dataset.label === 'Amount'
                        ? sortedData.map((item) => item.amount)
                        : sortedData.map((item) => item.price), // Cập nhật dữ liệu
                })),
            }));
        } else {
            // Sắp xếp mặc định theo Price
            const defaultData = rawData;

            setChartData((prev) => ({
                ...prev,
                labels: defaultData.map((item) =>
                    item.product.length > 10 ? item.product.slice(0, 10) + '...' : item.product
                ),
                datasets: prev.datasets.map((dataset) => ({
                    ...dataset,
                    data: dataset.label === 'Amount'
                        ? defaultData.map((item) => item.amount)
                        : defaultData.map((item) => item.price),
                })),
            }));
        }
    }, [hiddenDatasets, rawData]);

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
                onClick: handleLegendClick, // Xử lý sự kiện click
                labels: {
                    font: {
                        size: 16,
                    },
                    color: 'rgba(0, 0, 0, 0.7)',
                },
            },
            title: {
                display: true,
                text: 'Top 10 Products by Price and Amount',
                font: {
                    size: 20,
                },
                color: 'rgba(0, 0, 0, 0.8)',
                padding: {
                    top: 20,
                    bottom: 30,
                },
            },
            tooltip: {
                callbacks: {
                    // Tùy chỉnh tooltip để hiển thị tên đầy đủ của sản phẩm
                    title: (tooltipItem) => {
                        const productName = rawData[tooltipItem[0].dataIndex].product;
                        return productName;  // Hiển thị tên đầy đủ
                    },
                    label: (tooltipItem) => {
                        const datasetLabel = tooltipItem.dataset.label;
                        const value = tooltipItem.raw;
                        return `${datasetLabel}: ${datasetLabel === 'Price ($)' ? '$' : ''}${value}`;
                    },
                },
            },
        },
        scales: {
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    font: {
                        size: 14,
                    },
                },
            },
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function (value) {
                        return hiddenDatasets.includes(0) ? value : `$${value}`; // Định dạng cho trục y
                    },
                    font: {
                        size: 14,
                    },
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                },
            },
        },
        animation: {
            duration: 1000,
            easing: 'easeInOutBounce',
        },
        layout: {
            padding: {
                top: 40,
                left: 20,
                right: 20,
            },
        },
    };


    const filteredData = {
        ...chartData,
        datasets: chartData.datasets.map((dataset, index) => ({
            ...dataset,
            hidden: hiddenDatasets.includes(index), // Ẩn dataset nếu chỉ mục nằm trong `hiddenDatasets`
        })),
    };

    return (
        <div className="chart-container">
            <Bar data={filteredData} options={options} />
        </div>
    );
}

export default PriceClusterChart;
