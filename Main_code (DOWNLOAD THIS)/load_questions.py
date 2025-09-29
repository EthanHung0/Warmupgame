from pickle import dump

questions = [
    {
        "q": "Con vật nào là loài động vật lớn nhất trên Trái Đất?",
        "answer": "A",
        "options": ["A. Cá voi xanh", "B. Voi", "C. Cá mập", "D. Gấu bắc cực"]
    },
    {
        "q": "Quốc gia nào có diện tích lớn nhất thế giới?",
        "answer": "C",
        "options": ["A. Hoa Kỳ", "B. Trung Quốc", "C. Nga", "D. Canada"]
    },
    {
        "q": "Thủ đô của Pháp là gì?",
        "answer": "B",
        "options": ["A. London", "B. Paris", "C. Berlin", "D. Rome"]
    },
    {
        "q": "Quốc gia nào là nơi sản xuất cà phê lớn nhất thế giới?",
        "answer": "A",
        "options": ["A. Brazil", "B. Colombia", "C. Việt Nam", "D. Ấn Độ"]
    },
    {
        "q": "Bộ môn thể thao nào được coi là 'vua của các môn thể thao'?",
        "answer": "A",
        "options": ["A. Bóng đá", "B. Bóng rổ", "C. Quần vợt", "D. Cầu lông"]
    },
    {
        "q": "Nước nào được biết tới là có tượng nữ thần tự do?",
        "answer": "C",
        "options": ["A. Paris", "B. London", "C. New York", "D. Tokyo"]
    },
    {
        "q": "Ai ghi bàn nhiều nhất lịch sử bóng đá?",
        "answer": "A",
        "options": ["A. C. Ronaldo", "B. L. Messi", "C. Josef Bican", "D. Romário"]
    },
    {
        "q": "Nam Cao là tác giả của tác phẩm nào đã được học trong sách Ngữ văn 11?",
        "answer": "C",
        "options": ["A. Lão Hạc", "B. Vợ nhặt", "C. Chí Phèo", "D. Đời thừa"]
    },
    {
        "q": "Quê của nhà văn Kim Lân là tỉnh nào?",
        "answer": "A",
        "options": ["A. Bắc Ninh", "B. Bắc Giang", "C. Hà Nội", "D. Hải Dương"]
    },
    {
        "q": "Bức tranh 'Đêm đầy sao' do ai vẽ?",
        "answer": "C",
        "options": ["A. L. da Vinci", "B. P. Picasso", "C. V. van Gogh", "D. Claude Monet"]
    },
    {
        "q": "Bức tường Berlin dùng để làm gì?",
        "answer": "B.",
        "options": ["A. Bảo vệ người dân Đức", "B. Ngăn cách Đông và Tây Đức", "C. Ngăn quân Pháp xâm lược", "D. Là biểu tượng hòa bình"]
    },
    {
        "q": "Cơ quan nào có chức năng lọc máu?",
        "answer": "D",
        "options": ["A. Tim", "B. Phổi", "C. Gan", "D. Thận"]
    },
    {
        "q": "Cơ quan nào có chức năng tống máu đi khắp cơ thể?",
        "answer": "B",
        "options": ["A. Gan", "B. Tim", "C. Não", "D. Thận"]
    },
    {
        "q": "Loài động vật nào đứng để ngủ?",
        "answer": "B",
        "options": ["A. Bò", "B. Ngựa", "C. Voi", "D. Hươu cao cổ"]
    },
    {
        "q": "Ngày Nhà giáo Việt Nam là ngày nào?",
        "answer": "B",
        "options": ["A. 20/10", "B. 20/11", "C. 26/3", "D. 2/9"]
    },
    {
        "q": "Ngày 20/10 là ngày gì?",
        "answer": "B",
        "options": ["A. Giải phóng miền Nam", "B. Phụ nữ Việt Nam", "C. Quốc tế Lao động", "D. Quốc tế Phụ nữ"]
    },
    {
        "q": "Dãy núi nào cao nhất thế giới?",
        "answer": "C",
        "options": ["A. Andes", "B. Alps", "C. Himalaya", "D. Everest"]
    },
    {
        "q": "Ai là người đầu tiên đặt chân lên Mặt Trăng?",
        "answer": "A",
        "options": ["A. Neil Armstrong", "B. Yuri Gagarin", "C. Buzz Aldrin", "D. Michael Collins"]
    },
    {
        "q": "Việt Nam giành chức vô địch AFF Cup lần đầu tiên vào năm nào?",
        "answer": "C",
        "options": ["A. 1998", "B. 2004", "C. 2008", "D. 2018"]
    },
    {
        "q": "Quốc gia nào có nhiều dân số nhất thế giới (tính đến 2025)?",
        "answer": "A",
        "options": ["A. Ấn Độ", "B. Trung Quốc", "C. Hoa Kỳ", "D. Indonesia"]
    },
    {
        "q": "Ai được mệnh danh là 'Ông vua nhạc Pop'?",
        "answer": "B",
        "options": ["A. Elvis Presley", "B. Michael Jackson", "C. Freddie Mercury", "D. Justin Timberlake"]
    },
    {
        "q": "Năm 1945, sự kiện lịch sử nào diễn ra ở Việt Nam?",
        "answer": "D",
        "options": ["A. Chiến thắng ĐBPhủ", "B. Thành lập Đảng Cộng sản VN", "C. Ký kết hiệp định Genève", "D. Cm Tháng Tám"]
    },
    {
        "q": "Ngọn núi cao nhất Việt Nam là gì?",
        "answer": "B",
        "options": ["A. Bạch Mã", "B. Phan Xi Păng (Fansipan)", "C. Langbiang", "D. Ngọc Linh"]
    },
    {
        "q": "Ai là tác giả của tập truyện 'Nhật ký trong tù'?",
        "answer": "A",
        "options": ["A. Hồ Chí Minh", "B. Tố Hữu", "C. Xuân Diệu", "D. Nam Cao"]
    },
    {
        "q": "Nước nào đăng cai World Cup 2022?",
        "answer": "D",
        "options": ["A. Nga", "B. Mỹ", "C. Nhật Bản", "D. Qatar"]
    },
    {
        "q": "Sau khi sáp nhập năm 2023, thành phố Nha Trang hiện có bao nhiêu phường?",
        "answer": "C",
        "options": ["A. 23 phường", "B. 21 phường", "C. 19 phường", "D. 17 phường"]
    },
    {
        "q": "Tháng cô hồn rơi vào tháng mấy?",
        "answer": "B",
        "options": ["A. Tháng 9", "B. Tháng 7 âm lịch", "C. Tháng 8", "D. Tháng 8 âm lịch"]
    },
    {
        "q": "Tác giả của bài Bình Ngô Đại Cáo là ai?",
        "answer": "B",
        "options": ["A. Kim Lân", "B. Nguyễn Trãi", "C. Nam Cao", "D. Huy Cận"]
    },
    {
        "q": "Pytago là nhà gì?",
        "answer": "A",
        "options": ["A. Triết & toán học Hy Lạp cổ", "B. Nhà văn", "C. Triết học", "D. Thiên văn học"]
    },
    {
        "q": "Bác Hồ mất năm bao nhiêu?",
        "answer": "D",
        "options": ["A. 1970", "B. 1965", "C. 1960", "D. 1969"]
    },
    {
        "q": "Bác Hồ là nhà gì?",
        "answer": "B",
        "options": ["A. Nhà thơ", "B. CM & chính khách người VNm", "C. Nhà toán học", "D. Nhà vật lí"]
    },
    {
        "q": "Albert Einstein là nhà gì?",
        "answer": "C",
        "options": ["A. Nhà toán học", "B. Nhà văn", "C. Nhà vật lí", "D. Nhà triết học"]
    },
    {
        "q": "Cái gì luôn ở trước mặt bạn nhưng bạn không bao giờ thấy nó?",
        "answer": "A",
        "options": ["A. Tương lai", "B. Tin tức", "C. Gương", "D. Bóng tôi"]
    },
    {
        "q": "Cái gì càng nhiều càng nhẹ?",
        "answer": "C",
        "options": ["A. Sắt", "B. Lông vũ", "C. Lỗ hổng", "D. Nước"]
    },
    {
        "q": "Cái gì có nhiều thành phần nhưng không hề nặng, có thể dùng để che mưa?",
        "answer": "A",
        "options": ["A. Ô (dù)", "B. Quần áo", "C. Mũ bảo hiểm", "D. Túi nilon"]
    },
    {
        "q": "Một chiếc thuyền chở gạch nhưng không ướt; vì sao?",
        "answer": "C",
        "options": ["A. Gạch không thấm nước", "B. Thuyền có mái che", "C. Vì gạch chưa rơi xuống nước", "D. Thuyền không trên sông"]
    },
    {
        "q": "Thương hiệu xe nào nổi tiếng tiên phong về xe điện toàn cầu?",
        "answer": "B",
        "options": ["A. Toyota", "B. Tesla", "C. Ford", "D. BMW"]
    },
    {
        "q": "Công nghệ nào cho phép thanh toán chỉ cần chạm điện thoại vào máy quét?",
        "answer": "A",
        "options": ["A. NFC", "B. QR Code", "C. Bluetooth", "D. WiFi"]
    },
    {
        "q": "Loại kính thực tế ảo tăng cường (AR) đầu tiên Google giới thiệu năm 2013 tên là?",
        "answer": "B",
        "options": ["A. Google Lens", "B. Google Glass", "C. Google VR", "D. Google Pixel"]
    },
    {
        "q": "Công nghệ 5G so với 4G nổi bật nhờ đặc điểm nào?",
        "answer": "A",
        "options": ["A. Tốc độ cao, độ trễ thấp", "B. Chỉ dùng gọi điện thoại", "C. Rẻ hơn 3G", "D. Không cần internet"]
    },
    {
        "q": "Cái gì bạn dùng hằng ngày nhưng hầu như không nhìn thấy nó?",
        "answer": "D",
        "options": ["A. Dữ liệu số", "B. Pin điện thoại", "C. WiFi", "D. Điện"]
    },
    {
        "q": "Hệ điều hành nào sau đây KHÔNG phải là mã nguồn mở (open source)?",
        "answer": "C",
        "options": ["A. Linux", "B. Android", "C. iOS", "D. Ubuntu"]
    }
]


with open("Questions.pkl", "wb") as f:
    dump(questions,f)