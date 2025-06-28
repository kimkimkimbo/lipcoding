# 프로필 이미지 검증 유틸리티
from PIL import Image
import io

def validate_profile_image(file_storage):
    # 파일 확장자 및 mimetype 체크
    filename = file_storage.filename.lower()
    mimetype = file_storage.mimetype
    if not (filename.endswith('.jpg') or filename.endswith('.png')):
        return False, '이미지 확장자는 .jpg, .png만 허용됩니다.'
    if mimetype not in ['image/jpeg', 'image/png']:
        return False, '이미지 형식은 jpg, png만 허용됩니다.'
    # 파일 크기 체크 (1MB 이하)
    file_storage.seek(0, 2)
    size = file_storage.tell()
    if size > 1024*1024:
        return False, '이미지 크기는 1MB 이하만 허용됩니다.'
    file_storage.seek(0)
    # 이미지 해상도 및 정사각형 체크
    try:
        img = Image.open(file_storage)
        width, height = img.size
        if width != height:
            return False, '이미지는 정사각형이어야 합니다.'
        if width < 500 or width > 1000:
            return False, '이미지 해상도는 500~1000px만 허용됩니다.'
    except Exception:
        return False, '이미지 파일이 올바르지 않습니다.'
    file_storage.seek(0)
    return True, ''
