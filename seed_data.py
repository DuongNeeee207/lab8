import os
import sys
import django

# Thiết lập mã hóa UTF-8 cho console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashionstore.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
from products.models import Category, Product, ProductVariant

def seed():
    print("=== BẮT ĐẦU KHỞI TẠO DỮ LIỆU MẪU FASHIONSTORE ===")

    # 1. Tạo tài khoản Admin & Khách hàng mẫu
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@fashionstore.com',
            'first_name': 'Quản Trị',
            'last_name': 'Viên',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("-> Đã tạo tài khoản Admin: username='admin' / password='admin123'")
    else:
        print("-> Tài khoản Admin 'admin' đã tồn tại.")

    customer_user, created = User.objects.get_or_create(
        username='khachhang',
        defaults={
            'email': 'khachhang@example.com',
            'first_name': 'Nguyễn Văn',
            'last_name': 'An',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        customer_user.set_password('customer123')
        customer_user.save()
        customer_user.profile.phone_number = '0987654321'
        customer_user.profile.address = 'Số 68 Đường Cầu Giấy, Phường Dịch Vọng, Quận Cầu Giấy, Hà Nội'
        customer_user.profile.save()
        print("-> Đã tạo tài khoản Khách hàng: username='khachhang' / password='customer123'")

    # 2. Tạo các Danh mục thời trang
    categories_data = [
        {
            'name': 'Áo Sơ Mi (Shirts)',
            'slug': 'ao-so-mi',
            'description': 'Các dòng áo sơ mi công sở và dạo phố phom dáng Slim-fit, Regular chất liệu Oxford và Linen thoáng mát.'
        },
        {
            'name': 'Áo Thun & Polo (T-Shirts)',
            'slug': 'ao-thun',
            'description': 'Áo thun cotton 100% 250gsm co giãn 4 chiều, thấm hút mồ hôi tối ưu cho mùa hè năng động.'
        },
        {
            'name': 'Áo Hoodie & Sweatshirt',
            'slug': 'ao-hoodie',
            'description': 'Áo nỉ chui đầu và áo khoác hoodie form rộng trẻ trung phong cách Streetwear tối giản.'
        },
        {
            'name': 'Áo Khoác & Blazer (Jackets & Coats)',
            'slug': 'ao-khoac',
            'description': 'Blazer 2 lớp phong cách Hàn Quốc và áo khoác dạ ấm áp cho những ngày se lạnh.'
        },
        {
            'name': 'Quần Jeans & Quần Tây (Trousers)',
            'slug': 'quan-jeans-quan-tay',
            'description': 'Quần âu may đo chuẩn chỉ và quần jeans denim dày dặn bền bỉ.'
        },
        {
            'name': 'Váy & Đầm (Dresses & Skirts)',
            'slug': 'vay-dam',
            'description': 'Đầm suông linen, chân váy midi xòe nhẹ nhàng tôn lên nét nữ tính thanh lịch.'
        },
        {
            'name': 'Phụ Kiện Thời Trang (Accessories)',
            'slug': 'phu-kien',
            'description': 'Thắt lưng da bò, mũ lưỡi trai và túi canvas thời trang cao cấp.'
        }
    ]

    cat_map = {}
    for cdata in categories_data:
        cat, _ = Category.objects.get_or_create(
            slug=cdata['slug'],
            defaults={'name': cdata['name'], 'description': cdata['description']}
        )
        cat_map[cdata['slug']] = cat
    print(f"-> Đã kiểm tra/tạo {len(cat_map)} danh mục thời trang.")

    # 3. Tạo các Sản phẩm mẫu & Biến thể (Size & Màu & Tồn kho)
    products_data = [
        {
            'category': cat_map['ao-so-mi'],
            'name': 'Áo Sơ Mi Nam Oxford Dài Tay Cổ Điển',
            'slug': 'ao-so-mi-nam-oxford-dai-tay',
            'description': 'Áo sơ mi nam chất liệu Oxford dệt vân nổi cao cấp, phom dáng Slim-fit trẻ trung. Thích hợp đi làm công sở hoặc gặp gỡ đối tác trang trọng. Chống nhăn nhẹ sau khi giặt.',
            'price': 450000,
            'sale_price': 380000,
            'variants': [
                {'size': 'S', 'color': 'Trắng', 'sku': 'FS-SHIRT-WHT-S', 'stock': 15},
                {'size': 'M', 'color': 'Trắng', 'sku': 'FS-SHIRT-WHT-M', 'stock': 25},
                {'size': 'L', 'color': 'Trắng', 'sku': 'FS-SHIRT-WHT-L', 'stock': 20},
                {'size': 'M', 'color': 'Xanh Nhạt', 'sku': 'FS-SHIRT-BLU-M', 'stock': 18},
                {'size': 'L', 'color': 'Xanh Nhạt', 'sku': 'FS-SHIRT-BLU-L', 'stock': 12},
            ]
        },
        {
            'category': cat_map['ao-thun'],
            'name': 'Áo Thun Trơn Heavyweight 100% Cotton 250GSM',
            'slug': 'ao-thun-tron-heavyweight-cotton',
            'description': 'Chất vải dệt cotton chải kỹ định lượng 250gsm dầy dặn, không bai dão cổ áo sau nhiều lần giặt. Form áo Regular unisex phù hợp cho cả nam và nữ.',
            'price': 250000,
            'sale_price': 199000,
            'variants': [
                {'size': 'M', 'color': 'Đen', 'sku': 'FS-TEE-BLK-M', 'stock': 40},
                {'size': 'L', 'color': 'Đen', 'sku': 'FS-TEE-BLK-L', 'stock': 35},
                {'size': 'XL', 'color': 'Đen', 'sku': 'FS-TEE-BLK-XL', 'stock': 20},
                {'size': 'M', 'color': 'Trắng', 'sku': 'FS-TEE-WHT-M', 'stock': 30},
                {'size': 'L', 'color': 'Trắng', 'sku': 'FS-TEE-WHT-L', 'stock': 25},
            ]
        },
        {
            'category': cat_map['ao-khoac'],
            'name': 'Áo Khoác Blazer Nam Cổ Điển 2 Lớp',
            'slug': 'ao-khoac-blazer-nam-co-dien',
            'description': 'Mẫu Blazer hiện đại may 2 lớp lót lụa mềm mại, đệm vai tinh tế giúp tạo form đứng dáng tự nhiên. Sự kết hợp hoàn hảo cùng áo thun trắng và quần tây.',
            'price': 890000,
            'sale_price': 790000,
            'variants': [
                {'size': 'M', 'color': 'Đen', 'sku': 'FS-BLZ-BLK-M', 'stock': 10},
                {'size': 'L', 'color': 'Đen', 'sku': 'FS-BLZ-BLK-L', 'stock': 15},
                {'size': 'XL', 'color': 'Đen', 'sku': 'FS-BLZ-BLK-XL', 'stock': 8},
                {'size': 'L', 'color': 'Xám Đậm', 'sku': 'FS-BLZ-GRY-L', 'stock': 12},
            ]
        },
        {
            'category': cat_map['quan-jeans-quan-tay'],
            'name': 'Quần Tây Nam Dáng Ôm Xếp Ly Smart Casual',
            'slug': 'quan-tay-nam-xep-ly-smart-casual',
            'description': 'Quần tây vải tuyết mưa nhập khẩu mềm mịn, co giãn nhẹ không xù lông. Cạp quần trang bị đai tăng giảm thông minh tạo cảm giác thoải mái khi ngồi làm việc.',
            'price': 520000,
            'sale_price': 450000,
            'variants': [
                {'size': 'M', 'color': 'Đen', 'sku': 'FS-PAN-BLK-M', 'stock': 18},
                {'size': 'L', 'color': 'Đen', 'sku': 'FS-PAN-BLK-L', 'stock': 22},
                {'size': 'XL', 'color': 'Đen', 'sku': 'FS-PAN-BLK-XL', 'stock': 10},
                {'size': 'M', 'color': 'Xám Tro', 'sku': 'FS-PAN-GRY-M', 'stock': 14},
            ]
        },
        {
            'category': cat_map['vay-dam'],
            'name': 'Đầm Suông Linen Cổ Chữ V Tối Giản',
            'slug': 'dam-suong-linen-co-chu-v',
            'description': 'Đầm dáng suông may từ vải sợi Linen tưng tự nhiên cao cấp, thoáng mát tuyệt đối dưới tiết trời mùa hè. Thiết kế cổ V thanh thoát tôn bờ vai thon gọn.',
            'price': 650000,
            'sale_price': 560000,
            'variants': [
                {'size': 'S', 'color': 'Beige', 'sku': 'FS-DRS-BEI-S', 'stock': 12},
                {'size': 'M', 'color': 'Beige', 'sku': 'FS-DRS-BEI-M', 'stock': 16},
                {'size': 'L', 'color': 'Beige', 'sku': 'FS-DRS-BEI-L', 'stock': 10},
                {'size': 'M', 'color': 'Trắng Kem', 'sku': 'FS-DRS-WHT-M', 'stock': 14},
            ]
        },
        {
            'category': cat_map['ao-hoodie'],
            'name': 'Áo Hoodie Nỉ Bông Dáng Rộng Streetwear',
            'slug': 'ao-hoodie-ni-bong-dang-rong',
            'description': 'Chất liệu nỉ cotton lót bông dày dặn giữ ấm tốt. Mũ trùm đầu 2 lớp đứng form kèm túi kangaroo tiện lợi trước bụng.',
            'price': 480000,
            'sale_price': None,
            'variants': [
                {'size': 'M', 'color': 'Xám', 'sku': 'FS-HOD-GRY-M', 'stock': 20},
                {'size': 'L', 'color': 'Xám', 'sku': 'FS-HOD-GRY-L', 'stock': 25},
                {'size': 'XL', 'color': 'Đen', 'sku': 'FS-HOD-BLK-XL', 'stock': 15},
            ]
        },
        {
            'category': cat_map['quan-jeans-quan-tay'],
            'name': 'Quần Jeans Nam Ống Suông Vải Denim Selvedge',
            'slug': 'quan-jeans-nam-ong-suong-denim',
            'description': 'Denim 14oz bền bỉ, nhuộm chàm cổ điển. Form ống suông Straight-fit dễ dàng phối cùng mọi dòng giày sneaker hay bốt da.',
            'price': 580000,
            'sale_price': 490000,
            'variants': [
                {'size': 'M', 'color': 'Xanh Đậm', 'sku': 'FS-JNS-BLU-M', 'stock': 15},
                {'size': 'L', 'color': 'Xanh Đậm', 'sku': 'FS-JNS-BLU-L', 'stock': 18},
                {'size': 'XL', 'color': 'Xanh Đậm', 'sku': 'FS-JNS-BLU-XL', 'stock': 10},
            ]
        },
        {
            'category': cat_map['phu-kien'],
            'name': 'Thắt Lưng Da Bò Khóa Kim Loại Tối Giản',
            'slug': 'that-lung-da-bo-khoa-kim-loai',
            'description': '100% da bò tự nhiên nguyên miếng, mặt khóa hợp kim không rỉ mạ xước mờ sang trọng.',
            'price': 320000,
            'sale_price': 270000,
            'variants': [
                {'size': 'FREESIZE', 'color': 'Đen', 'sku': 'FS-BLT-BLK-FS', 'stock': 30},
                {'size': 'FREESIZE', 'color': 'Nâu Da Bò', 'sku': 'FS-BLT-BRN-FS', 'stock': 25},
            ]
        }
    ]

    for pdata in products_data:
        prod, p_created = Product.objects.get_or_create(
            slug=pdata['slug'],
            defaults={
                'category': pdata['category'],
                'name': pdata['name'],
                'description': pdata['description'],
                'price': pdata['price'],
                'sale_price': pdata['sale_price'],
                'is_active': True,
            }
        )
        if p_created or prod.variants.count() == 0:
            for vdata in pdata['variants']:
                ProductVariant.objects.get_or_create(
                    sku=vdata['sku'],
                    defaults={
                        'product': prod,
                        'size': vdata['size'],
                        'color': vdata['color'],
                        'stock_quantity': vdata['stock'],
                    }
                )
    print(f"-> Đã kiểm tra/tạo {len(products_data)} sản phẩm thời trang và đầy đủ các biến thể size/màu!")
    print("=== HOÀN TẤT KHỞI TẠO DỮ LIỆU THÀNH CÔNG ===")

if __name__ == '__main__':
    seed()
