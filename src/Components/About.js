import React from 'react';
import './CSS/About.css';

function About() {
    return (
        <div className="about-section">
            <div className="about-title">
                <h1>About</h1>
                <h2>Ecomlytics</h2>
            </div>

            <p>
                Dự án này là một phần quan trọng trong hành trình học tập của tôi với đề tài "Sales Data Analysis On E-Commerce Platform". Trang web này được thiết kế nhằm cung cấp một nền tảng trực quan và dễ tiếp cận để phân tích dữ liệu bán hàng trên các sản phẩm từ nền tảng thương mại điện tử Amazon. Với hơn 500,000 dữ liệu, dự án của tôi tập trung vào việc phân tích xu hướng, đánh giá sản phẩm tiềm năng, và khám phá những yếu tố tạo nên các sản phẩm bán chạy.
            </p>
        </div>
    );
}

export default About;
