import re
from email.utils import parseaddr

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


def is_valid_email(email: str) -> bool:
    if not email or '@' not in parseaddr(email)[1]:
        return False
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None


def is_valid_password(password: str) -> bool:
    # 8자 이상, 영문/숫자/특수문자 조합 권장
    return bool(password and len(password) >= 8)


def is_valid_role(role: str) -> bool:
    return role in {"mentor", "mentee"}


def is_valid_name(name: str) -> bool:
    return bool(name and 1 <= len(name) <= 30)


def is_valid_intro(intro: str) -> bool:
    return bool(intro and 1 <= len(intro) <= 200)


def is_valid_stack(stack: str) -> bool:
    # 쉼표로 구분된 기술스택, 각 항목 1~20자, 전체 100자 이하
    if not stack or len(stack) > 100:
        return False
    items = [s.strip() for s in stack.split(',')]
    return all(1 <= len(s) <= 20 for s in items if s)


def is_valid_image(filename: str, mimetype: str, size: int, width: int, height: int) -> (bool, str):
    ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    if f'.{ext}' not in ALLOWED_IMAGE_EXTENSIONS:
        return False, "이미지 확장자는 jpg, png만 허용됩니다."
    if size > 1024 * 1024:
        return False, "이미지 크기는 1MB 이하만 허용됩니다."
    if width != height or width < 500 or width > 1000:
        return False, "이미지는 정사각형 500~1000픽셀만 허용됩니다."
    return True, ""
