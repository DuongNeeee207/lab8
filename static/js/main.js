// ==========================================================================
// FASHIONSTORE CLIENT-SIDE INTERACTIONS (SMOOTH & RESPONSIVE)
// ==========================================================================

// Global functions for search panel - Đảm bảo gọi được từ mọi nơi và không bị lỗi
window.toggleExpandableSearch = function (e) {
    if (e && typeof e.preventDefault === 'function') {
        e.preventDefault();
        e.stopPropagation();
    }
    const panel = document.getElementById('expandableSearchPanel');
    if (!panel) return;
    if (panel.classList.contains('is-open')) {
        window.closeExpandableSearch();
    } else {
        window.openExpandableSearch();
    }
};

window.openExpandableSearch = function () {
    const panel = document.getElementById('expandableSearchPanel');
    const input = document.getElementById('expandableSearchInput');
    if (!panel) return;

    // Đóng bất kỳ dropdown nào đang mở để không che chắn
    const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
    openDropdowns.forEach(function (dd) {
        const toggle = dd.closest('.dropdown')?.querySelector('[data-bs-toggle="dropdown"]');
        if (toggle && window.bootstrap && bootstrap.Dropdown) {
            const inst = bootstrap.Dropdown.getInstance(toggle);
            if (inst) inst.hide();
        }
    });

    panel.classList.add('is-open');
    panel.setAttribute('aria-hidden', 'false');
    if (input) {
        setTimeout(function () {
            input.focus();
        }, 100);
    }
};

window.closeExpandableSearch = function () {
    const panel = document.getElementById('expandableSearchPanel');
    if (!panel) return;
    panel.classList.remove('is-open');
    panel.setAttribute('aria-hidden', 'true');
};

document.addEventListener('DOMContentLoaded', function () {
    // 1. Gắn sự kiện click cho nút Search Desktop & Mobile
    const searchToggleBtn = document.getElementById('searchToggleBtn');
    if (searchToggleBtn) {
        searchToggleBtn.addEventListener('click', function (e) {
            window.toggleExpandableSearch(e);
        });
    }

    const searchCloseBtn = document.getElementById('searchCloseBtn');
    if (searchCloseBtn) {
        searchCloseBtn.addEventListener('click', function (e) {
            if (e) e.stopPropagation();
            window.closeExpandableSearch();
        });
    }

    // Đóng khi click ra ngoài panel tìm kiếm
    document.addEventListener('click', function (e) {
        const panel = document.getElementById('expandableSearchPanel');
        const btn = document.getElementById('searchToggleBtn');
        if (panel && panel.classList.contains('is-open')) {
            if (!panel.contains(e.target) && (!btn || !btn.contains(e.target))) {
                window.closeExpandableSearch();
            }
        }
    });

    // Đóng khi nhấn phím ESC
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            const panel = document.getElementById('expandableSearchPanel');
            if (panel && panel.classList.contains('is-open')) {
                window.closeExpandableSearch();
            }
        }
    });

    // 2. Tự động ẩn thông báo flash message sau 4 giây
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 4000);
    });

    // 3. Cập nhật thông tin biến thể khi người dùng chọn kích cỡ hoặc màu sắc
    const variantRadios = document.querySelectorAll('input[name="variant_id"]');
    const stockInfoDisplay = document.getElementById('variant-stock-info');
    const addToCartBtn = document.getElementById('add-to-cart-btn');

    if (variantRadios.length > 0 && stockInfoDisplay) {
        variantRadios.forEach(function (radio) {
            radio.addEventListener('change', function () {
                const stock = parseInt(this.getAttribute('data-stock') || '0', 10);
                if (stock > 0) {
                    stockInfoDisplay.innerHTML = `<span class="text-success fw-semibold"><i class="bi bi-check-circle-fill me-1"></i> Còn hàng (${stock} sản phẩm sẵn có tại kho)</span>`;
                    if (addToCartBtn) addToCartBtn.disabled = false;
                } else {
                    stockInfoDisplay.innerHTML = `<span class="text-danger fw-semibold"><i class="bi bi-x-circle-fill me-1"></i> Hết hàng - Vui lòng chọn phân loại khác</span>`;
                    if (addToCartBtn) addToCartBtn.disabled = true;
                }
            });
        });
    }

    // 4. Back To Top Button mượt mà
    const btnBackToTop = document.getElementById('btnBackToTop');
    if (btnBackToTop) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 300) {
                btnBackToTop.classList.add('is-visible');
            } else {
                btnBackToTop.classList.remove('is-visible');
            }
        }, { passive: true });

        btnBackToTop.addEventListener('click', function (e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});
