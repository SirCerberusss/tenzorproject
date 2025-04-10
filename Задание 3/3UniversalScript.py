import json
import os

def parse_template(template):
    parts = template.split(".")
    generated = []
    for val in [1, 2]:  # Просто два варианта замены '*'
        new_parts = []
        for part in parts:
            if part == "*":
                new_parts.append(str(val))
            else:
                new_parts.append(part)
        generated.append(".".join(new_parts))
    return generated

def version_to_list(version):
    return [int(x) for x in version.split(".")]

def main():
    # Данные ввода
    input_version = input("Введите номер версии продукта (например, 3.7.2): ").strip()
    config_file = input("Введите имя конфигурационного файла (например, config.json): ").strip()

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_config_path = os.path.join(script_dir, config_file)
        with open(full_config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        print("Ошибка при чтении файла конфигурации:", e)
        return

    all_versions = []

    for key in config:
        template = config[key]
        generated = parse_template(template)
        all_versions.extend(generated)

    # Удаляет дубликаты
    all_versions = list(set(all_versions))
    all_versions.sort(key=lambda v: version_to_list(v))

    print("\nВсе сгенерированные версии:")
    for ver in all_versions:
        print(ver)

    print(f"\nВерсии меньше чем {input_version}:")
    input_ver_list = version_to_list(input_version)
    for ver in all_versions:
        if version_to_list(ver) < input_ver_list:
            print(ver)

if __name__ == "__main__":
    main()
