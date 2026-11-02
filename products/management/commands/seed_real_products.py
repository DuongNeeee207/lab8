"""
Management command: seed_real_products
Thêm dữ liệu sản phẩm thật (tên, mô tả, giá, ảnh) vào database.
Ảnh được download từ Unsplash về thư mục media/products/.
Chạy: python manage.py seed_real_products
"""
import os
import uuid
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from products.models import Category, Product, ProductVariant


# ---------------------------------------------------------------------------
# DỮ LIỆU SẢN PHẨM THẬT
# Ảnh Unsplash - public domain, không cần API key
# ---------------------------------------------------------------------------

PRODUCT_DATA = {
    # -----------------------------------------------------------------------
    # ÁO THUN
    # -----------------------------------------------------------------------
    "ao-thun": [
        {
            "name": "Áo Thun Basic Trắng Cổ Tròn",
            "description": "Áo thun basic cổ tròn chất liệu cotton 100% cao cấp, mềm mịn, thấm hút mồ hôi tốt. Thiết kế tối giản phù hợp mọi phong cách. Form regular fit thoải mái cho cả nam và nữ.",
            "price": 189000,
            "sale_price": 149000,
            "colors": ["Trắng", "Đen", "Xám"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80",
        },
        {
            "name": "Áo Thun Oversize Đen Unisex",
            "description": "Áo thun oversize form rộng phong cách Hàn Quốc, chất liệu cotton pha spandex co giãn nhẹ. Phù hợp mặc đi chơi, đi học hay đi làm casual.",
            "price": 229000,
            "sale_price": 189000,
            "colors": ["Đen", "Trắng", "Navy"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=800&q=80",
        },
        {
            "name": "Áo Thun Polo Nam Cổ Bẻ",
            "description": "Áo polo nam cổ bẻ 2 nút chất liệu pique cotton cao cấp. Dáng slim fit thanh lịch, phù hợp đi làm, đi chơi hoặc các sự kiện semi-formal.",
            "price": 299000,
            "sale_price": 249000,
            "colors": ["Trắng", "Navy", "Xanh lá"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=800&q=80",
        },
        {
            "name": "Áo Thun Nữ Croptop Cơ Bản",
            "description": "Áo thun croptop nữ dáng ngắn ngang eo, chất cotton mềm mại co giãn 4 chiều. Kết hợp hoàn hảo với quần jeans, chân váy hay quần short.",
            "price": 165000,
            "sale_price": 129000,
            "colors": ["Trắng", "Đen", "Hồng", "Be"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&q=80",
        },
        {
            "name": "Áo Thun Kẻ Sọc Ngang Classic",
            "description": "Áo thun kẻ sọc ngang phong cách Breton cổ điển, chất cotton dày dặn không bai nhão. Mang lại vẻ ngoài năng động, trẻ trung và thời trang.",
            "price": 219000,
            "sale_price": None,
            "colors": ["Xanh-Trắng", "Đen-Trắng", "Đỏ-Trắng"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800&q=80",
        },
        {
            "name": "Áo Thun In Hình Streetwear",
            "description": "Áo thun unisex in hình graphic streetwear độc đáo, chất liệu cotton 220gsm dày dặn. Wash được nhiều lần không phai màu, không bong tróc.",
            "price": 259000,
            "sale_price": 219000,
            "colors": ["Trắng", "Đen"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800&q=80",
        },
        {
            "name": "Áo Thun Nữ Cổ V Mềm Mại",
            "description": "Áo thun nữ cổ V dáng regular, chất modal cotton cao cấp siêu mềm mịn như lụa. Màu sắc tươi sáng không bạc màu, phù hợp mặc đi làm hay dạo phố.",
            "price": 199000,
            "sale_price": 159000,
            "colors": ["Trắng", "Đen", "Xám", "Xanh nhạt"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1485218126466-34e6392ec754?w=800&q=80",
        },
        {
            "name": "Áo Thun Nam Pocket Tee",
            "description": "Áo thun nam có túi ngực nhỏ phong cách vintage, chất cotton wash mềm mại. Thiết kế đơn giản nhưng tinh tế, phù hợp phong cách everyday casual.",
            "price": 210000,
            "sale_price": 179000,
            "colors": ["Xanh wash", "Xám", "Nâu đất"],
            "sizes": ["M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&q=80",
        },
        {
            "name": "Áo Thun Longsleeve Thu Đông",
            "description": "Áo thun tay dài chất cotton pha lycra giữ ấm tốt, co giãn 4 chiều thoải mái. Thiết kế tối giản dễ mix & match với mọi outfit.",
            "price": 239000,
            "sale_price": 195000,
            "colors": ["Đen", "Trắng", "Xám đậm", "Navy"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&q=80",
        },
        {
            "name": "Áo Thun Thể Thao Dry-Fit",
            "description": "Áo thun thể thao chất liệu polyester dry-fit thoát hơi nhanh, chống tia UV. Phù hợp tập gym, chạy bộ, đạp xe hay các hoạt động ngoài trời.",
            "price": 279000,
            "sale_price": 229000,
            "colors": ["Đen", "Xanh dương", "Đỏ", "Xám"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&q=80",
        },
        {
            "name": "Áo Thun Trẻ Em Bé Trai",
            "description": "Áo thun cho bé trai chất cotton organic mềm mại, an toàn cho làn da nhạy cảm. Màu sắc tươi sáng, hình in dễ thương, bền màu qua nhiều lần giặt.",
            "price": 145000,
            "sale_price": 119000,
            "colors": ["Xanh", "Đỏ", "Vàng"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1519278409-1f56ab241a7e?w=800&q=80",
        },
        {
            "name": "Áo Thun Linen Thoáng Mát Hè",
            "description": "Áo thun chất linen (vải lanh) tự nhiên siêu thoáng mát, thấm hút mồ hôi. Lý tưởng cho mùa hè nóng bức, càng mặc càng mềm và thoải mái.",
            "price": 325000,
            "sale_price": 275000,
            "colors": ["Trắng", "Be", "Xanh mint", "Vàng chanh"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1594938298603-c8148c4b4730?w=800&q=80",
        },
    ],

    # -----------------------------------------------------------------------
    # ÁO SƠ MI
    # -----------------------------------------------------------------------
    "ao-so-mi": [
        {
            "name": "Sơ Mi Trắng Oxford Nam",
            "description": "Áo sơ mi nam vải Oxford trắng cổ điển, chất cotton 100% dày dặn không nhìn thấu. Dáng slim fit thanh lịch, phù hợp đi làm văn phòng, diện trang trọng.",
            "price": 399000,
            "sale_price": 329000,
            "colors": ["Trắng"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&q=80",
        },
        {
            "name": "Sơ Mi Linen Dáng Suông Nữ",
            "description": "Áo sơ mi nữ chất linen tự nhiên dáng suông oversized, tay dài có thể xắn lên. Vẻ ngoài thanh lịch, thoáng mát, phù hợp đi làm hay đi dạo cuối tuần.",
            "price": 459000,
            "sale_price": 389000,
            "colors": ["Trắng", "Be nude", "Xanh nhạt"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=800&q=80",
        },
        {
            "name": "Sơ Mi Kẻ Caro Flannel Ấm",
            "description": "Áo sơ mi vải flannel kẻ caro giữ ấm tốt cho mùa thu đông, chất liệu mềm mại dễ chịu. Phong cách casual-chic phù hợp mặc đi chơi, dã ngoại.",
            "price": 349000,
            "sale_price": 299000,
            "colors": ["Đỏ-Đen", "Xanh-Đen", "Xanh-Trắng"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=800&q=80",
        },
        {
            "name": "Sơ Mi Nữ Bèo Ngực Dịu Dàng",
            "description": "Áo sơ mi nữ chất chiffon mềm nhẹ, điểm nhấn bèo nhỏ ở ngực tạo nét nữ tính. Dáng fit vừa vặn tôn dáng, phù hợp đi làm hay buổi hẹn hò.",
            "price": 289000,
            "sale_price": 239000,
            "colors": ["Trắng", "Hồng phấn", "Xanh mint"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1551489186-cf8726f514f8?w=800&q=80",
        },
        {
            "name": "Sơ Mi Nam Denim Nhẹ Mùa Hè",
            "description": "Áo sơ mi nam chất denim nhẹ mỏng, thiết kế túi ngực đặc trưng phong cách Americana. Mặc đơn hay layer cùng áo thun đều đẹp.",
            "price": 429000,
            "sale_price": None,
            "colors": ["Xanh nhạt", "Xanh đậm", "Trắng"],
            "sizes": ["M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&q=80",
        },
        {
            "name": "Sơ Mi Sọc Dọc Công Sở",
            "description": "Áo sơ mi kẻ sọc dọc fine stripe phong cách công sở sang trọng, chất cotton pha polyester chống nhăn. Dáng regular fit thoải mái, dễ phối đồ.",
            "price": 369000,
            "sale_price": 310000,
            "colors": ["Trắng-Xanh", "Trắng-Đen"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1607345366928-199ea26cfe3e?w=800&q=80",
        },
        {
            "name": "Sơ Mi Hawaiian Hoa Nhiệt Đới",
            "description": "Áo sơ mi họa tiết hoa lá nhiệt đới phong cách Hawaiian, chất viscose nhẹ mát. Mang lại cảm giác nghỉ dưỡng, phù hợp đi biển hay sự kiện outdoor.",
            "price": 319000,
            "sale_price": 269000,
            "colors": ["Xanh nhiệt đới", "Đỏ hoa", "Trắng hoa"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1563178406-4cdc2923acbc?w=800&q=80",
        },
        {
            "name": "Sơ Mi Cài Nút Ngọc Trai Nữ",
            "description": "Áo sơ mi nữ cài nút ngọc trai tinh tế, chất satin bóng nhẹ sang trọng. Phù hợp dự tiệc, sự kiện hay đi làm trong văn phòng.",
            "price": 489000,
            "sale_price": 399000,
            "colors": ["Trắng ngà", "Đen", "Xanh hoàng gia"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?w=800&q=80",
        },
        {
            "name": "Sơ Mi Ngắn Tay Resort Style",
            "description": "Áo sơ mi tay ngắn phong cách resort sang trọng, chất liệu nhẹ thoáng mát. Thiết kế đơn giản tinh tế, phù hợp du lịch hay dạo phố mùa hè.",
            "price": 359000,
            "sale_price": 299000,
            "colors": ["Trắng", "Be", "Xanh nhạt"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1621072156002-e2fccdc0b176?w=800&q=80",
        },
        {
            "name": "Sơ Mi Vintage Wash Denim",
            "description": "Áo sơ mi denim vintage wash phong cách retro cổ điển. Chất denim nhẹ được xử lý màu tạo hiệu ứng faded tự nhiên, càng mặc càng đẹp.",
            "price": 445000,
            "sale_price": 375000,
            "colors": ["Xanh faded", "Đen faded"],
            "sizes": ["M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&q=80",
        },
    ],

    # -----------------------------------------------------------------------
    # ÁO HOODIE & NỈ
    # -----------------------------------------------------------------------
    "ao-hoodie-ni": [
        {
            "name": "Hoodie Basic Unisex Màu Xám",
            "description": "Áo hoodie basic unisex chất nỉ bông dày 380gsm, lót bông mềm mịn bên trong. Mũ có dây rút điều chỉnh, túi kangaroo rộng rãi. Phù hợp mọi phong cách.",
            "price": 399000,
            "sale_price": 339000,
            "colors": ["Xám", "Đen", "Trắng", "Navy"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=800&q=80",
        },
        {
            "name": "Áo Nỉ Crewneck Sweater Nữ",
            "description": "Áo sweater cổ tròn crewneck nữ chất nỉ bông mềm mịn, form oversize thoải mái. Thiết kế minimal không họa tiết, dễ phối với mọi loại quần.",
            "price": 359000,
            "sale_price": 299000,
            "colors": ["Hồng pastel", "Be", "Xanh mint", "Tím nhạt"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=800&q=80",
        },
        {
            "name": "Hoodie In Logo Streetwear",
            "description": "Áo hoodie in logo to phong cách streetwear Mỹ, chất french terry 350gsm dày dặn. Màu sắc đậm không phai, wash nhiều lần vẫn giữ form và màu.",
            "price": 459000,
            "sale_price": 389000,
            "colors": ["Đen", "Trắng"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1509942774463-acf339cf87d5?w=800&q=80",
        },
        {
            "name": "Áo Zip-up Hoodie Nam Cao Cấp",
            "description": "Áo hoodie kéo khóa zip toàn thân, chất nỉ bông hai lớp ấm áp. Khóa YKK chất lượng cao, đường may tỉ mỉ, phù hợp mặc ở nhà hay ra ngoài.",
            "price": 479000,
            "sale_price": 399000,
            "colors": ["Xám", "Đen", "Navy"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800&q=80",
        },
        {
            "name": "Sweater Cổ Lọ Dệt Kim Thu Đông",
            "description": "Áo sweater cổ lọ chất len cashmere pha acrylic ấm áp, mềm mịn không gây ngứa. Thiết kế cổ lọ cao sang trọng, phù hợp mùa lạnh.",
            "price": 549000,
            "sale_price": 449000,
            "colors": ["Kem", "Caramel", "Xám đậm", "Đen"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=800&q=80",
        },
        {
            "name": "Hoodie Tie-dye Màu Sắc Sáng Tạo",
            "description": "Áo hoodie nhuộm tie-dye thủ công độc đáo, mỗi chiếc một màu riêng không chiếc nào giống nhau. Chất cotton nỉ bông dày, form oversize cool ngầu.",
            "price": 429000,
            "sale_price": 359000,
            "colors": ["Xanh-Tím", "Cam-Vàng", "Hồng-Đỏ"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=800&q=80",
        },
        {
            "name": "Áo Nỉ Thể Thao Nike-Style",
            "description": "Áo nỉ thể thao phong cách sport, chất polyester fleece nhẹ giữ ấm tốt. Phù hợp tập thể dục nhẹ, đi bộ hay mặc casual hàng ngày.",
            "price": 349000,
            "sale_price": 289000,
            "colors": ["Đen", "Xám", "Xanh dương"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80",
        },
        {
            "name": "Cardigan Len Mỏng Nữ Vintage",
            "description": "Áo cardigan nữ chất len mỏng phong cách vintage, thiết kế cài nút với túi ở hai bên. Dáng dài qua hông, phù hợp mặc mùa thu hoặc layer trong nhà.",
            "price": 399000,
            "sale_price": 329000,
            "colors": ["Vàng mustard", "Xanh sage", "Trắng kem"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=800&q=80",
        },
        {
            "name": "Hoodie Reflective Phản Quang",
            "description": "Áo hoodie có chi tiết phản quang ở logo và đường viền, an toàn khi đi ngoài ban đêm. Chất nỉ bông cao cấp, thiết kế futuristic độc đáo.",
            "price": 549000,
            "sale_price": 469000,
            "colors": ["Đen", "Xám đậm"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=800&q=80",
        },
        {
            "name": "Sweater Dệt Kim Caro Retro",
            "description": "Áo sweater dệt kim họa tiết caro phong cách vintage Anh Quốc. Chất len pha acrylic ấm áp, form boxy thoải mái, dễ phối đồ mùa lạnh.",
            "price": 489000,
            "sale_price": 399000,
            "colors": ["Nâu đỏ", "Xanh Navy"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1604644401890-0bd678c83788?w=800&q=80",
        },
    ],

    # -----------------------------------------------------------------------
    # ÁO KHOÁC & BLAZER
    # -----------------------------------------------------------------------
    "ao-khoac-blazer": [
        {
            "name": "Blazer Đen Công Sở Nam",
            "description": "Blazer nam vải tweed màu đen dáng slim fit thanh lịch, lót trong thoáng mát. Phù hợp đi làm, dự hội nghị hay các sự kiện trang trọng. Đường may tỉ mỉ, chất liệu cao cấp.",
            "price": 899000,
            "sale_price": 749000,
            "colors": ["Đen", "Xám đậm", "Navy"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80",
        },
        {
            "name": "Áo Khoác Denim Jean Jacket",
            "description": "Áo khoác denim kinh điển không bao giờ lỗi mốt, chất denim 12oz cứng cáp bền đẹp. Form regular fit truyền thống, túi ngực và túi hông tiện dụng.",
            "price": 599000,
            "sale_price": 499000,
            "colors": ["Xanh nhạt", "Xanh đậm", "Đen"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1548126032-079a0fb0099d?w=800&q=80",
        },
        {
            "name": "Blazer Nữ Linen Bộ Suits",
            "description": "Blazer nữ chất linen sang trọng thuộc bộ suits, dáng oversized hiện đại. Có thể mặc đơn lẻ hoặc phối cùng quần âu cùng chất. Phù hợp phong cách power dressing.",
            "price": 849000,
            "sale_price": 699000,
            "colors": ["Trắng kem", "Be sand", "Xanh sage"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800&q=80",
        },
        {
            "name": "Áo Khoác Bomber Unisex",
            "description": "Áo bomber unisex kiểu dáng phong cách, chất nylon nhẹ chống gió nhẹ. Cổ rib, tay rib, gấu rib đặc trưng. Phù hợp mùa thu hoặc thời tiết mát mẻ.",
            "price": 649000,
            "sale_price": 549000,
            "colors": ["Đen", "Xanh olive", "Đỏ đô"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80",
        },
        {
            "name": "Áo Khoác Gió Windbreaker Nhẹ",
            "description": "Áo khoác gió nhẹ chất nylon taffeta chống gió, chống nước nhẹ. Có thể gấp gọn bỏ túi, lý tưởng cho du lịch, đi phượt hay hoạt động ngoài trời.",
            "price": 479000,
            "sale_price": 399000,
            "colors": ["Đen", "Navy", "Xanh mint", "Cam"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1544966503-a2d8e77e96f0?w=800&q=80",
        },
        {
            "name": "Áo Phao Lông Vũ Siêu Nhẹ",
            "description": "Áo phao lông vũ trắng thiên ngỗng 90/10 siêu nhẹ siêu ấm. Có thể gấp vào túi đi kèm, thích hợp du lịch. Chống gió và nước tốt cho mùa đông.",
            "price": 1290000,
            "sale_price": 990000,
            "colors": ["Đen", "Trắng", "Navy", "Đỏ"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1547949003-9792a18a2601?w=800&q=80",
        },
        {
            "name": "Trench Coat Dài Thanh Lịch",
            "description": "Áo khoác trench coat dài qua gối phong cách Anh Quốc cổ điển, chất cotton twill dày dặn. Đai thắt eo tạo dáng thanh lịch, phù hợp đi làm hay sự kiện.",
            "price": 1490000,
            "sale_price": 1190000,
            "colors": ["Camel", "Đen", "Beige"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=800&q=80",
        },
        {
            "name": "Áo Khoác Da PU Nam Moto Style",
            "description": "Áo khoác da PU cao cấp phong cách motorcycle, khóa zip bất đối xứng cá tính. Lót lông bên trong ấm áp, phù hợp mùa thu đông phong cách rock.",
            "price": 899000,
            "sale_price": 749000,
            "colors": ["Đen", "Nâu đất"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1520975954732-35dd22299614?w=800&q=80",
        },
        {
            "name": "Blazer Kẻ Sọc Tweed Sang Trọng",
            "description": "Blazer kẻ sọc windowpane chất tweed cao cấp phong cách Anh Quốc. Nút vải, ve áo notch lapel, túi hộp. Dáng slim fit thanh lịch tôn dáng.",
            "price": 1190000,
            "sale_price": 950000,
            "colors": ["Xám", "Nâu"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1594938298603-c8148c4b4730?w=800&q=80",
        },
        {
            "name": "Áo Khoác Sherpa Teddy Ấm",
            "description": "Áo khoác sherpa teddy bear siêu ấm siêu mềm, lót và mặt ngoài đều là sherpa lông cừu nhân tạo. Form oversized dễ thương, phù hợp mùa đông lạnh giá.",
            "price": 749000,
            "sale_price": 619000,
            "colors": ["Trắng kem", "Nâu caramel"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1481349518771-20055b2a7b24?w=800&q=80",
        },
    ],

    # -----------------------------------------------------------------------
    # QUẦN JEANS & TÂY
    # -----------------------------------------------------------------------
    "quan-jeans-tay": [
        {
            "name": "Quần Jeans Nam Slim Fit Xanh Classic",
            "description": "Quần jeans nam dáng slim fit cổ điển, chất denim cotton 98% co giãn nhẹ thoải mái khi vận động. Đường may 5 túi truyền thống, wash standard xanh đẹp.",
            "price": 599000,
            "sale_price": 499000,
            "colors": ["Xanh classic", "Xanh đậm", "Đen"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&q=80",
        },
        {
            "name": "Quần Jeans Nữ Skinny High-Waist",
            "description": "Quần jeans nữ cạp cao skinny ôm dáng tôn vóc dáng, chất denim co giãn 4 chiều thoải mái. Cạp cao nhấn eo, phù hợi phối cùng áo thun, sơ mi hay crop top.",
            "price": 549000,
            "sale_price": 449000,
            "colors": ["Xanh nhạt", "Xanh đậm", "Đen", "Trắng"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?w=800&q=80",
        },
        {
            "name": "Quần Jeans Wide Leg Vintage",
            "description": "Quần jeans ống rộng phong cách vintage 90s, chất denim dày bền. Dáng straight leg rộng thoải mái, high waist tôn dáng, phù hợp mọi vóc dáng.",
            "price": 629000,
            "sale_price": 529000,
            "colors": ["Xanh faded", "Đen", "Trắng"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=800&q=80",
        },
        {
            "name": "Quần Âu Nam Slim Fit Công Sở",
            "description": "Quần tây nam dáng slim fit vải tropical wool phong cách công sở. Ống bó vừa phải tôn dáng, chất liệu cao cấp chống nhăn tốt, đứng form suốt ngày làm việc.",
            "price": 699000,
            "sale_price": 589000,
            "colors": ["Đen", "Xám", "Navy"],
            "sizes": ["S", "M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1594938298603-c8148c4b4730?w=800&q=80",
        },
        {
            "name": "Quần Jogger Nỉ Thoải Mái",
            "description": "Quần jogger chất nỉ bông co giãn tốt, gấu bo rib đặc trưng phong cách athleisure. Túi bên và túi sau tiện dụng, phù hợp tập gym, ở nhà hay đi phố casual.",
            "price": 349000,
            "sale_price": 299000,
            "colors": ["Xám", "Đen", "Navy"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=800&q=80",
        },
        {
            "name": "Quần Short Jean Nữ Ripped",
            "description": "Quần short jeans nữ có rách nhẹ phong cách bohemian, cạp cao tôn dáng. Chất denim nhẹ thoáng mát lý tưởng cho mùa hè, beach vacation hay đi phố.",
            "price": 349000,
            "sale_price": 279000,
            "colors": ["Xanh nhạt", "Trắng"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1591195853828-11db59a44f43?w=800&q=80",
        },
        {
            "name": "Quần Jeans Nam Straight Fit Ripped",
            "description": "Quần jeans thẳng có chi tiết rách gối và đùi phong cách casual-cool. Chất denim rigid bền chắc, wash medium blue đẹp cổ điển.",
            "price": 579000,
            "sale_price": 479000,
            "colors": ["Xanh medium"],
            "sizes": ["M", "L", "XL"],
            "img_url": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=800&q=80",
        },
        {
            "name": "Quần Âu Nữ Ống Suông Linen",
            "description": "Quần âu nữ ống suông chất linen tự nhiên, thoáng mát nhẹ nhàng. Thiết kế cạp cao với ly trước tạo vẻ sang trọng, thanh lịch phù hợp đi làm hay sự kiện.",
            "price": 559000,
            "sale_price": 469000,
            "colors": ["Trắng", "Be", "Đen"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&q=80",
        },
        {
            "name": "Quần Cargo Multi-Pocket",
            "description": "Quần cargo nhiều túi phong cách military, chất cotton twill bền chắc. 6 túi tiện dụng, dây rút gấu tiện chỉnh độ dài. Phù hợp outdoor, phượt, đi dã ngoại.",
            "price": 499000,
            "sale_price": 419000,
            "colors": ["Khaki", "Đen", "Olive"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "img_url": "https://images.unsplash.com/photo-1519975258993-60b42d1c2ee2?w=800&q=80",
        },
        {
            "name": "Quần Jeans Mom Jean Cạp Cao",
            "description": "Quần mom jean cạp cao form rộng ở hông thu hẹp dần về gấu, phong cách retro chic. Chất denim rigid vintage wash tạo vẻ đặc trưng thập niên 80-90.",
            "price": 589000,
            "sale_price": 489000,
            "colors": ["Xanh vintage", "Đen wash"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1560243563-062bfc001d68?w=800&q=80",
        },
    ],

    # -----------------------------------------------------------------------
    # VÁY & ĐẦM
    # -----------------------------------------------------------------------
    "vay-dam": [
        {
            "name": "Đầm Maxi Hoa Nhí Boho",
            "description": "Đầm maxi dài chấm gót họa tiết hoa nhí phong cách bohemian, chất viscose nhẹ mát rượi. Dây đan cổ gợi cảm thanh lịch, phù hợp đi biển, du lịch hay sự kiện ngoài trời.",
            "price": 599000,
            "sale_price": 499000,
            "colors": ["Trắng hoa", "Xanh hoa", "Vàng hoa"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=800&q=80",
        },
        {
            "name": "Chân Váy Midi Plissé Xếp Ly",
            "description": "Chân váy midi xếp ly accordion chất satin bóng nhẹ, dài qua gối thanh lịch. Cạp chun co giãn thoải mái, phù hợp đi làm, dự tiệc hay chụp ảnh lookbook.",
            "price": 449000,
            "sale_price": 369000,
            "colors": ["Đen", "Be satin", "Xanh hoàng gia", "Đỏ đô"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=800&q=80",
        },
        {
            "name": "Đầm Cổ Chữ V Wrap Dress",
            "description": "Đầm wrap cổ chữ V quyến rũ, chất jersey mềm rũ ôm nhẹ theo cơ thể. Thiết kế quấn thắt eo tạo dáng đồng hồ cát thanh lịch, phù hợp mọi dịp.",
            "price": 529000,
            "sale_price": 439000,
            "colors": ["Đen", "Đỏ rượu", "Xanh navy"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&q=80",
        },
        {
            "name": "Chân Váy Mini Denim A-line",
            "description": "Chân váy jeans mini dáng A xòe nhẹ, chất denim cotton dày dặn. Phối cùng áo thun, áo crop top hay sơ mi đều tạo ra outfit trendy, năng động.",
            "price": 349000,
            "sale_price": 289000,
            "colors": ["Xanh nhạt", "Đen", "Trắng"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1591195853828-11db59a44f43?w=800&q=80",
        },
        {
            "name": "Đầm Linen Dáng Suông Mùa Hè",
            "description": "Đầm suông cổ tròn không tay chất linen tự nhiên siêu thoáng mát, dài qua gối. Phong cách minimalist nhẹ nhàng thanh lịch, lý tưởng cho ngày hè oi bức.",
            "price": 489000,
            "sale_price": 399000,
            "colors": ["Trắng", "Be", "Xanh nhạt", "Cam đất"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=800&q=80",
        },
        {
            "name": "Váy Babydoll Hoa Nhỏ Vintage",
            "description": "Đầm babydoll cổ vuông viền bèo nhỏ họa tiết hoa nhỏ vintage, phong cách tiểu thư Cottagecore. Tay bồng nhẹ xinh xắn, chất cotton mềm mát dễ chịu.",
            "price": 429000,
            "sale_price": 359000,
            "colors": ["Trắng hoa", "Xanh hoa"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=800&q=80",
        },
        {
            "name": "Đầm Cocktail Sequin Lấp Lánh",
            "description": "Đầm cocktail đính sequin toàn thân lấp lánh sang trọng, dáng bodycon tôn dáng. Phù hợp dự tiệc, sự kiện, Gala dinner hay các dịp đặc biệt.",
            "price": 899000,
            "sale_price": 749000,
            "colors": ["Bạc", "Vàng gold", "Đen sequin"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=800&q=80",
        },
        {
            "name": "Chân Váy Len Kẻ Caro Thu Đông",
            "description": "Chân váy len kẻ caro midi phong cách preppy Anh Quốc, chất len mềm giữ ấm. Dài qua gối thanh lịch, phối cùng áo len hay sơ mi đều chuẩn style.",
            "price": 499000,
            "sale_price": 419000,
            "colors": ["Đỏ caro", "Xanh caro", "Be caro"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=800&q=80",
        },
        {
            "name": "Đầm Satin Cúp Ngực Sang Trọng",
            "description": "Đầm cúp ngực chất satin bóng mịn cao cấp, phong cách tối giản sang trọng. Thiết kế không tay, dây mảnh ở lưng, dài qua gối. Phù hợp dự tiệc hay hẹn hò.",
            "price": 749000,
            "sale_price": 619000,
            "colors": ["Đen", "Champagne", "Đỏ merlot"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1571513722275-4b41940f54b8?w=800&q=80",
        },
        {
            "name": "Chân Váy Thun Midi Basic",
            "description": "Chân váy thun midi cơ bản cạp chun co giãn thoải mái, dài qua gối. Chất thun co giãn 4 chiều ôm dáng đẹp. Dễ phối đồ, phù hợp đi làm hay đi chơi.",
            "price": 259000,
            "sale_price": 209000,
            "colors": ["Đen", "Trắng", "Be", "Xám"],
            "sizes": ["S", "M", "L"],
            "img_url": "https://images.unsplash.com/photo-1544441893-675973e31985?w=800&q=80",
        },
    ],

    # -----------------------------------------------------------------------
    # PHỤ KIỆN THỜI TRANG
    # -----------------------------------------------------------------------
    "phu-kien-thoi-trang": [
        {
            "name": "Túi Tote Canvas Minimalist",
            "description": "Túi tote vải canvas dày dặn phong cách tối giản, đủ lớn đựng laptop 13 inch và phụ kiện. Quai túi chắc chắn thoải mái khi đeo, có túi nhỏ bên trong tiện lợi.",
            "price": 299000,
            "sale_price": 249000,
            "colors": ["Trắng", "Đen", "Be"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800&q=80",
        },
        {
            "name": "Mũ Bucket Hat Vải Chống Nắng",
            "description": "Mũ bucket hat vành tròn chống nắng UPF50+, chất cotton dày thoáng khí. Vành rộng che khuất cổ và vai, lý tưởng cho đi biển, đi dã ngoại hay đi phố mùa hè.",
            "price": 199000,
            "sale_price": 159000,
            "colors": ["Trắng", "Đen", "Beige", "Xanh mint"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1521369909029-2afed882baee?w=800&q=80",
        },
        {
            "name": "Thắt Lưng Da Bò Genuine Leather",
            "description": "Thắt lưng da bò thật 100% Genuine Leather bền đẹp, mặt khóa khắc logo tinh tế. Rộng 3.5cm phù hợp quần âu và jeans. Tặng kèm hộp đựng cao cấp.",
            "price": 459000,
            "sale_price": 389000,
            "colors": ["Đen", "Nâu"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=80",
        },
        {
            "name": "Khăn Quàng Cổ Len Cashmere",
            "description": "Khăn quàng cổ len cashmere mềm mịn không gây ngứa, giữ ấm tuyệt vời mùa lạnh. Kích thước lớn 180x70cm có thể quấn nhiều kiểu khác nhau.",
            "price": 349000,
            "sale_price": 289000,
            "colors": ["Xám", "Camel", "Đen", "Đỏ"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=800&q=80",
        },
        {
            "name": "Kính Mát Polarized UV400",
            "description": "Kính mát tròng phân cực polarized chống tia UV400 bảo vệ mắt tối đa. Gọng kim loại mỏng nhẹ thời trang, phù hợp nhiều kiểu mặt. Kèm hộp cứng và khăn lau.",
            "price": 399000,
            "sale_price": 329000,
            "colors": ["Đen-Đen", "Vàng-Nâu", "Bạc-Xám"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&q=80",
        },
        {
            "name": "Túi Xách Crossbody Da PU",
            "description": "Túi đeo chéo crossbody chất da PU cao cấp mềm mịn bền đẹp. Ngăn chính rộng + ngăn phụ phía trước, dây đeo có thể điều chỉnh độ dài. Phù hợp đi làm, đi chơi.",
            "price": 549000,
            "sale_price": 449000,
            "colors": ["Đen", "Nâu caramel", "Be"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=800&q=80",
        },
        {
            "name": "Mũ Cói Đi Biển Rộng Vành",
            "description": "Mũ cói đan tay thủ công vành rộng phong cách boho đi biển. Vành 15cm che nắng hiệu quả, dây rút điều chỉnh kích cỡ. Dễ gấp bỏ vali khi du lịch.",
            "price": 259000,
            "sale_price": 219000,
            "colors": ["Tự nhiên", "Nhuộm đen"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1434510423563-23e1be3e6a47?w=800&q=80",
        },
        {
            "name": "Balo Laptop Chống Nước",
            "description": "Balo đa năng chống nước chứa laptop đến 15.6 inch, chất liệu polyester 1680D bền chắc. Ngăn USB sạc ngoài tiện lợi, nhiều ngăn phụ phân loại đồ gọn gàng.",
            "price": 699000,
            "sale_price": 589000,
            "colors": ["Đen", "Xám"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=80",
        },
        {
            "name": "Vòng Tay Bạc 925 Minimal",
            "description": "Vòng tay bạc 925 sterling thiết kế tối giản thanh lịch. Khắc chữ tinh tế, không gây dị ứng da, phù hợp đeo hàng ngày. Hộp quà cao cấp phù hợp làm gift.",
            "price": 299000,
            "sale_price": None,
            "colors": ["Bạc"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=800&q=80",
        },
        {
            "name": "Dây Chuyền Vàng 10K Thanh Lịch",
            "description": "Dây chuyền vàng 10K thật kiểu dây rolo mảnh thanh lịch, dài 45cm có khóa tôm. Không bị xỉn màu, chứng nhận vàng thật kèm tem bảo hành 12 tháng.",
            "price": 1290000,
            "sale_price": None,
            "colors": ["Vàng"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&q=80",
        },
        {
            "name": "Ví Da Nam Slim Wallet",
            "description": "Ví da nam dạng slim mỏng chất da bò thật, chứa đến 8 thẻ + ngăn tiền mặt. Thiết kế RFID blocking bảo vệ thông tin thẻ ngân hàng. Kích thước siêu gọn bỏ túi trước.",
            "price": 389000,
            "sale_price": 319000,
            "colors": ["Đen", "Nâu"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&q=80",
        },
        {
            "name": "Nón Snapback Streetwear 6-Panel",
            "description": "Nón snapback 6 panel phong cách streetwear, thêu logo phẳng ở mặt trước cá tính. Khóa snapback điều chỉnh vừa mọi đầu, lưỡi chai phẳng đặc trưng.",
            "price": 229000,
            "sale_price": 189000,
            "colors": ["Đen", "Trắng", "Navy"],
            "sizes": ["FREESIZE"],
            "img_url": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=800&q=80",
        },
    ],
}


class Command(BaseCommand):
    help = "Seed dữ liệu sản phẩm thật với ảnh từ Unsplash"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Xóa toàn bộ sản phẩm hiện có trước khi seed",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("⚠️  Đang xóa toàn bộ sản phẩm cũ..."))
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✅ Đã xóa xong."))

        # Tạo thư mục lưu ảnh nếu chưa có
        media_root = getattr(settings, "MEDIA_ROOT", "media")
        products_img_dir = os.path.join(media_root, "products")
        os.makedirs(products_img_dir, exist_ok=True)

        total_created = 0
        total_variants = 0

        for cat_slug, products in PRODUCT_DATA.items():
            # Tìm category theo slug (thử nhiều dạng slug)
            category = self._get_category(cat_slug)
            if not category:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Không tìm thấy danh mục slug='{cat_slug}', bỏ qua.")
                )
                continue

            self.stdout.write(f"\n📂 Danh mục: {category.name}")

            for p_data in products:
                product, created = Product.objects.get_or_create(
                    name=p_data["name"],
                    defaults={
                        "category": category,
                        "description": p_data["description"],
                        "price": p_data["price"],
                        "sale_price": p_data.get("sale_price"),
                        "is_active": True,
                    },
                )

                if not created:
                    self.stdout.write(f"   ↩️  Đã tồn tại: {product.name}")
                else:
                    # Download ảnh
                    img_path = self._download_image(
                        p_data["img_url"], products_img_dir, product
                    )
                    if img_path:
                        rel_path = os.path.relpath(img_path, media_root)
                        product.image = rel_path.replace("\\", "/")
                        product.save()

                    total_created += 1
                    self.stdout.write(f"   ✅ Tạo: {product.name}")

                    # Tạo variants (size × color)
                    sizes = p_data.get("sizes", ["S", "M", "L"])
                    colors = p_data.get("colors", ["Đen"])
                    sku_counter = 0
                    for color in colors:
                        for size in sizes:
                            sku_counter += 1
                            sku = f"{product.id}-{size}-{color[:3].upper()}-{sku_counter}"
                            variant, v_created = ProductVariant.objects.get_or_create(
                                product=product,
                                size=size,
                                color=color,
                                defaults={
                                    "sku": sku,
                                    "stock_quantity": 25,
                                },
                            )
                            if v_created:
                                total_variants += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Hoàn thành! Đã tạo {total_created} sản phẩm và {total_variants} biến thể."
            )
        )

    # Mapping từ slug trong PRODUCT_DATA → slug thật trong DB
    SLUG_MAP = {
        "ao-thun": "ao-thun",               # ID=2: Áo Thun & Polo
        "ao-so-mi": "ao-so-mi",             # ID=1: Áo Sơ Mi
        "ao-hoodie-ni": "ao-hoodie",        # ID=3: Áo Hoodie & Nỉ
        "ao-khoac-blazer": "ao-khoac",      # ID=4: Áo Khoác & Blazer
        "quan-jeans-tay": "quan-jeans-quan-tay",  # ID=5: Quần Jeans & Tây
        "vay-dam": "vay-dam",               # ID=6: Váy & Đầm
        "phu-kien-thoi-trang": "phu-kien",  # ID=7: Phụ Kiện Thời Trang
    }

    def _get_category(self, slug):
        """Tìm category theo slug mapping."""
        real_slug = self.SLUG_MAP.get(slug, slug)
        cat = Category.objects.filter(slug=real_slug).first()
        if cat:
            return cat
        # Fallback: tìm theo tên chứa keyword
        keyword_map = {
            "ao-thun": "Thun",
            "ao-so-mi": "Sơ Mi",
            "ao-hoodie-ni": "Hoodie",
            "ao-khoac-blazer": "Khoác",
            "quan-jeans-tay": "Jeans",
            "vay-dam": "Váy",
            "phu-kien-thoi-trang": "Phụ",
        }
        keyword = keyword_map.get(slug, "")
        if keyword:
            cat = Category.objects.filter(name__icontains=keyword).first()
        return cat

    def _download_image(self, url, save_dir, product):
        """Download ảnh từ URL về thư mục local."""
        try:
            filename = f"product_{product.id}_{uuid.uuid4().hex[:8]}.jpg"
            filepath = os.path.join(save_dir, filename)
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                with open(filepath, "wb") as f:
                    f.write(response.read())
            self.stdout.write(f"      📷 Tải ảnh: {filename}")
            return filepath
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"      ⚠️  Không tải được ảnh: {e}")
            )
            return None
