import os
import zipfile
from datetime import datetime, timezone

ZIP_PATH = "netflix_cookie.zip"

def is_cookie_valid(content):
    """
    يفحص إذا كان الحساب شغالاً وغير منتهي الصلاحية بناءً على تاريخ Valid Till
    """
    has_valid_date = True
    for line in content.splitlines():
        if "valid till" in line.lower():
            try:
                # مثال: Valid Till (UTC): 2026-10-10 16:43:30 UTC
                parts = line.split(":", 1)
                if len(parts) > 1:
                    date_str = parts[1].replace("UTC", "").replace("utc", "").strip()
                    exp_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    # إذا كان تاريخ الانتهاء أقل من الوقت الحالي (انتهى)، يعتبر غير شغال
                    if exp_date < datetime.now(timezone.utc):
                        return False 
            except Exception as e:
                print(f"خطأ في قراءة التاريخ: {e}")
    
    # التأكد من وجود كوكيز صالحة للنتفليكس بداخل الملف
    if "NetflixId" in content or "NFToken" in content:
        return has_valid_date
    return False

def main():
    if not os.path.exists(ZIP_PATH):
        print("ملف الـ ZIP غير موجود!")
        return

    valid_files = {}
    removed_count = 0

    # قراءة ملف الـ ZIP الحالي
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        for filename in zf.namelist():
            if filename.endswith('/') or filename.startswith('__MACOSX'):
                continue
            content = zf.read(filename).decode('utf-8', errors='ignore')
            
            # فحص الحساب
            if is_cookie_valid(content):
                valid_files[filename] = content
            else:
                removed_count += 1

    print(f"إجمالي الحسابات الشغالة التي تم الاحتفاظ بها: {len(valid_files)}")
    print(f"إجمالي الحسابات المنتهية التي تم حذفها: {removed_count}")

    # إعادة إنشاء ملف الـ ZIP بالحسابات الشغالة فقط
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename, content in valid_files.items():
            zf.writestr(filename, content)

    print("تم تحديث ملف netflix_cookie.zip بنجاح!")

if __name__ == "__main__":
    main()
