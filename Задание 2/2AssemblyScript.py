import os
import json
import shutil
from datetime import datetime
import subprocess

def log(msg):
    """Выводит сообщение с текущим временем"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def check_repo(url):
    """Проверка доступности репозитория"""
    try:
        url = url if url.endswith('.git') else f"{url}.git"
        log("Проверяем доступность репозитория...")
        return subprocess.run(["git", "ls-remote", url], 
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE).returncode == 0
    except Exception as e:
        log(f"Ошибка при проверке репозитория: {str(e)}")
        return False

def force_remove(path):
    """Рекурсивно удаляет папку со всеми файлами"""
    if not os.path.exists(path):
        return
    log(f"Удаляем папку {os.path.basename(path)}...")
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.chmod(file_path, 0o777)
            os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            os.chmod(dir_path, 0o777)
            os.rmdir(dir_path)
    os.rmdir(path)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_folder = os.path.join(script_dir, "temp_repo")
    
    log("=== Начало работы скрипта ===")
    log(f"Рабочая директория: {script_dir}")

    # Проверка репозитория
    while True:
        repo_url = input("[Введите адрес репозитория]: ").strip()
        if check_repo(repo_url):
            log("Репозиторий доступен!")
            break
        log("Ошибка: Репозиторий не найден! Пример: https://github.com/user/repo")

    # Клонирование
    force_remove(temp_folder)
    log("Клонируем репозиторий...")
    subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_folder], check=True)
    log("Клонирование завершено")
    
    # Проверка пути
    while True:
        target_path = input("[Введите путь внутри репозитория]: ").strip()
        full_path = os.path.join(temp_folder, target_path)
        if os.path.exists(full_path):
            log(f"Путь '{target_path}' найден")
            break
        log(f"Ошибка: Путь '{target_path}' не существует! Доступные:")
        print('\n'.join(os.listdir(temp_folder)))
    
    version = input("[Введите версию продукта]: ").strip()
    folder_name = os.path.basename(target_path)
    
    # Создаем version.json
    log("Формируем список файлов...")
    files = [
        os.path.relpath(os.path.join(root, f), full_path).replace("\\", "/")
        for root, _, files in os.walk(full_path)
        for f in files if f.endswith(('.py', '.js', '.sh'))
    ]
    log("Создаем version.json...")
    with open(os.path.join(full_path, "version.json"), 'w') as f:
        json.dump({"name": folder_name, "version": version, "files": files}, f, indent=2)
    log("version.json успешно создан")
    
    # Создаем архив
    os.chdir(script_dir)
    archive_name = f"{folder_name}_{datetime.now().strftime('%Y%m%d')}.zip"
    log(f"Создаем архив {archive_name}...")
    shutil.make_archive(archive_name[:-4], "zip", full_path)
    log("Архив успешно создан")
    
    # Очистка
    log("Очищаем временные файлы...")
    force_remove(temp_folder)
    
    # Итог
    log(f"=== Готово ===")
    log(f"Архив создан: {archive_name}")
    log(f"Расположение: {os.path.join(script_dir, archive_name)}")
    if os.name == 'nt':
        log("Открываем проводник...")
        os.startfile(script_dir)

if __name__ == "__main__":
    main()