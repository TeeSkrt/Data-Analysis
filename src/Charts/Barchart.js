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

    const fetchData = async () => {
        try {
            const response = await fetch('https://bedata.azurewebsites.net/api/getdata/?format=json&page=1');
            const data = await response.json();
            const allData = data.data;

            const topProducts = allData
                .sort((a, b) => b.price - a.price)
                .slice(0, 10);

            const labels = topProducts.map((item) => item.product);
            const prices = topProducts.map((item) => item.price);
            const amounts = topProducts.map((item) => item.amount);

            setChartData({
                labels,
                datasets: [
                    {
                        label: 'Price ($)',
                        data: prices,
                        backgroundColor: 'rgba(123, 104, 238, 0.7)',  // Lighter color for better readability
                        borderColor: 'rgba(123, 104, 238, 1)',
                        borderWidth: 1,
                        barPercentage: 0.35,
                        hoverBackgroundColor: 'rgba(123, 104, 238, 1)', // Add hover effect
                    },
                    {
                        label: 'Amount',
                        data: amounts,
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

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    font: {
                        size: 16,   // Increase font size for better readability
                    },
                    color: 'rgba(0, 0, 0, 0.7)',  // Darker text for better contrast
                },
            },
            title: {
                display: true,
                text: 'Top 10 Products by Price and Quantity',
                font: {
                    size: 20,   // Increase the font size for the title
                },
                color: 'rgba(0, 0, 0, 0.8)',  // Dark color for the title
                padding: {
                    top: 20,    // Add more space on top to ensure title is not cut off
                    bottom: 30, // Add space below the title
                },
            },
        },
        scales: {
            x: {
                grid: {
                    display: false,  // Hide gridlines on x-axis for a cleaner look
                },
                ticks: {
                    font: {
                        size: 14,   // Adjust font size for x-axis labels
                    },
                },
            },
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function (value) {
                        return value % 1 === 0 ? `$${value}` : value; // Display currency format for price
                    },
                    font: {
                        size: 14,   // Adjust font size for y-axis labels
                    },
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)', // Lighter gridlines for better visibility
                },
            },
        },
        animation: {
            duration: 1000,  // Add smooth animation duration
            easing: 'easeInOutBounce',  // Make the animation smooth and bouncy
        },
        layout: {
            padding: {
                top: 40,   // Add padding to the top for the title to fit well
                left: 20,  // Padding for left side
                right: 20, // Padding for right side
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
