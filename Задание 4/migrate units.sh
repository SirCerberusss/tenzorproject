#!/bin/bash

# Получаем все юниты с именем foobar-что_то
units=$(systemctl list-units --type=service --all | grep foobar- | awk '{print $1}')

for unit in $units; do
    echo "👉 Работаем с юнитом: $unit"

    # Сначала остановим его (чтоб ниче не поломалось)
    systemctl stop "$unit"

    # Путь до файла юнита
    unit_path=$(systemctl show -p FragmentPath "$unit" | cut -d'=' -f2)

    if [[ ! -f "$unit_path" ]]; then
        echo "❌ Юнит файл не найден: $unit_path (пропускаем)"
        continue
    fi

    # Получаем название сервиса без префикса
    service_name=$(echo "$unit" | sed 's/^foobar-//')

    old_dir="/opt/misc/$service_name"
    new_dir="/srv/data/$service_name"

    # Если старая директория есть - переносим
    if [[ -d "$old_dir" ]]; then
        echo "📦 Перемещаем $old_dir -> $new_dir"
        mv "$old_dir" "$new_dir"
    else
        echo "⚠️ Директория $old_dir не найдена, пропуск..."
        continue
    fi

    # Меняем пути в юнит файле
    echo "✏️ Обновляем пути в $unit_path"
    sed -i "s|WorkingDirectory=.*|WorkingDirectory=$new_dir|" "$unit_path"
    sed -i "s|ExecStart=.*|ExecStart=$new_dir/foobar-daemon произвольные_параметры|" "$unit_path"

    # Перезагрузка systemd (на всякий случай)
    systemctl daemon-reload

    # Запускаем сервис назад
    systemctl start "$unit"

    echo "✅ Готово: $unit"
    echo "-------------------------"
done
