import requests
from dotenv import load_dotenv, find_dotenv
from os import getenv


class RST:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.APPLICATION_ID = getenv("APPLICATION_ID")
        self.MASTER_KEY = getenv("MASTER_KEY")
        self.T_APPLICATION_ID = getenv("T_APPLICATION_ID")
        self.T_MASTER_KEY = getenv("T_MASTER_KEY")
        self.BASE_URL = getenv("BASE_URL")

    def get_headers(self, time=False):
        if time == False: return {
            "X-Parse-Application-Id": self.APPLICATION_ID,
            "X-Parse-Master-Key": self.MASTER_KEY,
            "Content-Type": "application/json"
        }
        else: return {
            "X-Parse-Application-Id": self.T_APPLICATION_ID,
            "X-Parse-Master-Key": self.T_MASTER_KEY,
            "Content-Type": "application/json"
        }

    def find_record_by_discordid(self, clname, discord_id):
        """Найти запись по DiscordID"""
        headers = self.get_headers()
        if clname == "Time": headers = self.get_headers(time=True)
        try:
            response = requests.get(
                f"{self.BASE_URL}{clname}",
                headers=headers,
                params={"where": f'{{"DiscordID":"{discord_id}"}}'}
            )
            response.raise_for_status()
            results = response.json().get("results", [])
            return results[0] if results else None
        except Exception as e:
            return f"Ошибка при поиске записи: {str(e)}"

    def get_dict_records(self, clname, field_name, isflt=False, convert_types=None, convert_index=None):
        """Получить словарь всех записей в формате {DiscordID: field_value} или {DiscordID: [field_value1, field_value2]}

        Args:
            clname: Название класса (таблицы)
            field_name: Название поля или список полей для получения
            isflt: Если True - преобразует все числовые значения в float (устаревший параметр)
            convert_types: Тип или список типов для преобразования значений
            convert_index: Индекс поля для преобразования (если None - преобразуются все подходящие)
        """
        headers = self.get_headers()
        if clname == "Time":
            headers = self.get_headers(time=True)

        try:
            response = requests.get(f"{self.BASE_URL}{clname}", headers=headers, params={"limit": 1000})
            response.raise_for_status()
            records = response.json().get("results", [])

            # Подготовка параметров преобразования типов
            if convert_types is not None:
                if not isinstance(convert_types, (list, tuple)):
                    # Если field_name - список, а convert_types - один тип, применяем его ко всем полям
                    if isinstance(field_name, (list, tuple)):
                        convert_types = [convert_types] * len(field_name)
                    else:
                        convert_types = [convert_types]
                elif isinstance(field_name, (list, tuple)) and len(convert_types) != len(field_name):
                    # Если количество типов не совпадает с количеством полей, применяем первый тип ко всем полям
                    convert_types = [convert_types[0]] * len(field_name)

            result_dict = {}

            for record in records:
                discord_id = record.get("DiscordID")

                # Если field_name - список полей
                if isinstance(field_name, (list, tuple)):
                    values = []
                    for i, field in enumerate(field_name):
                        value = record.get(field, "N/A")

                        # Преобразование типов
                        if convert_types is not None and (convert_index is None or convert_index == i):
                            try:
                                value = convert_types[i](value)
                            except (ValueError, TypeError):
                                pass
                        # Совместимость с isflt (для обратной совместимости)
                        elif isflt and i == 0:
                            try:
                                value = float(value)
                            except (ValueError, TypeError):
                                pass

                        values.append(value)

                    result_dict[discord_id] = values
                # Если field_name - одно поле
                else:
                    value = record.get(field_name, "N/A")

                    # Преобразование типов
                    if convert_types is not None and (convert_index is None or convert_index == 0):
                        try:
                            value = convert_types[0](value)
                        except (ValueError, TypeError):
                            pass
                    # Совместимость с isflt (для обратной совместимости)
                    elif isflt:
                        try:
                            value = float(value)
                        except (ValueError, TypeError):
                            pass

                    result_dict[discord_id] = value

            return result_dict

        except Exception as e:
            return f"Ошибка в get_dict_records: {str(e)}"

    def update_field_by_discordid(self, clname, discord_id, field_name, field_value, increment=True):
        """Обновить поле по DiscordID с возможностью добавления значения
        Args:
            clname: Название класса (таблицы)
            discord_id: ID пользователя Discord
            field_name: Название поля для обновления
            field_value: Значение для установки/добавления
            increment: Если True - добавляет field_value к текущему значению,
                       Если False - заменяет текущее значение (по умолчанию)
        """
        headers = self.get_headers()
        if clname == "Time": headers = self.get_headers(time=True)
        try:
            # Находим запись по DiscordID
            record = self.find_record_by_discordid(clname, discord_id)
            if not record or isinstance(record, str):
                return f"Запись с DiscordID {discord_id} не найдена"

            object_id = record["objectId"]

            # Если нужно добавить значение (инкремент)
            if increment:
                update_data = {
                    field_name: {
                        "__op": "Increment",
                        "amount": field_value
                    }
                }
            else:
                # Простая замена значения
                update_data = {field_name: field_value}

            response = requests.put(
                f"{self.BASE_URL}{clname}/{object_id}",
                headers=headers,
                json=update_data
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            return f"Ошибка при обновлении записи: {str(e)}"

    def create_record_with_discordid(self, clname, discord_id, initial_data=None):
        """Создать новую запись с указанным DiscordID"""
        headers = self.get_headers()
        if clname == "Time": headers = self.get_headers(time=True)
        data = {"DiscordID": discord_id}
        if initial_data:
            data.update(initial_data)

        try:
            response = requests.post(f"{self.BASE_URL}{clname}", headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Ошибка при создании записи: {str(e)}"

    def delete_record_by_discordid(self, clname, discord_id):
        """Удалить запись по DiscordID"""
        headers = self.get_headers()
        if clname == "Time": headers = self.get_headers(time=True)
        try:
            # Сначала находим запись по DiscordID
            record = self.find_record_by_discordid(clname, discord_id)
            if not record or isinstance(record, str):
                return f"Запись с DiscordID {discord_id} не найдена"

            # Удаляем запись по её objectId
            object_id = record["objectId"]
            response = requests.delete(f"{self.BASE_URL}{clname}/{object_id}", headers=headers)
            response.raise_for_status()
            return {"status": "success", "message": f"Запись с DiscordID {discord_id} удалена"}
        except Exception as e:
            return f"Ошибка при удалении записи: {str(e)}"


restapi_funcs = RST()