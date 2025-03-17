import random
import requests
import logging

logger = logging.getLogger(__name__)

# Map mã quốc gia và emoji
COUNTRY_MAP = {
    'us': 'Mỹ',
    'gb': 'Anh',
    'fr': 'Pháp',
    'de': 'Đức',
    'ca': 'Canada',
    'au': 'Úc',
    'br': 'Brazil',
    'mx': 'Mexico',
    'es': 'Tây Ban Nha',
    'nl': 'Hà Lan',
    'dk': 'Đan Mạch',
    'fi': 'Phần Lan',
    'ie': 'Ireland',
    'in': 'Ấn Độ',
    'ir': 'Iran',
    'no': 'Na Uy',
    'nz': 'New Zealand',
    'ch': 'Thụy Sĩ',
    'tr': 'Thổ Nhĩ Kỳ',
    'ua': 'Ukraine',
    'rs': 'Serbia'
}

COUNTRY_EMOJI = {
    'us': '🇺🇸',
    'gb': '🇬🇧',
    'fr': '🇫🇷',
    'de': '🇩🇪',
    'ca': '🇨🇦',
    'au': '🇦🇺',
    'br': '🇧🇷',
    'mx': '🇲🇽',
    'es': '🇪🇸',
    'nl': '🇳🇱',
    'dk': '🇩🇰',
    'fi': '🇫🇮',
    'ie': '🇮🇪',
    'in': '🇮🇳',
    'ir': '🇮🇷',
    'no': '🇳🇴',
    'nz': '🇳🇿',
    'ch': '🇨🇭',
    'tr': '🇹🇷',
    'ua': '🇺🇦',
    'rs': '🇷🇸'
}


def get_random_user(nat=None):
    """Lấy thông tin người dùng ngẫu nhiên từ RandomUser API."""
    url = "https://randomuser.me/api/"
    params = {"nat": nat} if nat else {}

    try:
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        logger.error(f"Lỗi API RandomUser: {e}")
        return None


def generate_cards_from_bin(bin_code, count=5):
    """Tạo số thẻ tín dụng dựa trên BIN với độ dài bất kỳ."""
    cards = []
    bin_length = len(bin_code)

    # Kiểm tra BIN chỉ chứa số
    if not bin_code.isdigit():
        raise ValueError("Mã BIN không hợp lệ. Vui lòng chỉ nhập số.")

    # Kiểm tra BIN không dài hơn 16 số
    if bin_length > 15:
        raise ValueError("Mã BIN quá dài. Vui lòng nhập ít hơn 16 số.")

    for _ in range(count):
        # Tạo phần còn lại của số thẻ (đảm bảo tổng cộng là 16 chữ số)
        remaining_digits = 16 - bin_length
        random_part = ''.join(
            [str(random.randint(0, 9)) for _ in range(remaining_digits - 1)])
        card_without_check = bin_code + random_part

        # Tính toán check digit (Luhn algorithm)
        total = 0
        for i, digit in enumerate(reversed(card_without_check)):
            n = int(digit)
            if i % 2 == 0:
                n *= 2
                if n > 9:
                    n -= 9
            total += n

        check_digit = (10 - (total % 10)) % 10
        card_number = card_without_check + str(check_digit)

        # Tạo ngày hết hạn ngẫu nhiên
        month = random.randint(1, 12)
        year = random.randint(2025, 2033)
        expiry_month = f"{month:02d}"
        expiry_year = f"{year}"

        # Tạo CVV ngẫu nhiên (3 chữ số)
        cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])

        cards.append({
            'number': card_number,  # Không có dấu cách
            'expiry_month': expiry_month,
            'expiry_year': expiry_year,
            'cvv': cvv
        })

    return cards
