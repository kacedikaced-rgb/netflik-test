import os
import zipfile

ZIP_PATH = "netflix_cookie.zip"

def is_cookie_valid(content):
    """
    التحقق من أن الملف يحتوي على بيانات نتفليكس سليمة (Token أو NetflixId)
    """
    if "NetflixId" in content or "NFToken" in content or "ct=" in content or "ct%3D" in content:
        return True
    return False

def main():
    if not os.path.exists(ZIP_PATH):
        print("ملف الـ ZIP غير موجود!")
        return

    valid_files = {}

    # قراءة ملف الـ ZIP الحالي
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        for filename in zf.namelist():
            if filename.endswith('/') or filename.startswith('__MACOSX'):
                continue
            content = zf.read(filename).decode('utf-8', errors='ignore')
            
            # فحص إذا كان الملف يحتوي على حساب صالح
            if is_cookie_valid(content):
                valid_files[filename] = content

    # صمام أمان: إذا كانت القائمة ستصبح فارغة، امنع الحذف تماماً وحافظ على الملف القديم!
    if not valid_files:
        print("تحذير: لم يتم العثور على حسابات صالحة أو أن القائمة فارغة. تم إلغاء التحديث لمنع تفريغ ملف الـ ZIP.")
        return

    print(f"إجمالي الحسابات الصالحة التي سيتم الاحتفاظ بها: {len(valid_files)}")

    # إعادة كتابة ملف الـ ZIP بالحسابات الصالحة فقط
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename, content in valid_files.items():
            zf.writestr(filename, content)

    print("تم تحديث ملف netflix_cookie.zip بنجاح دون تفريغه!")

if __name__ == "__main__":
    main()
