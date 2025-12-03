import csv
from datetime import datetime
import mysql.connector

config = {
    "user": "python_user",
    "password": "strong_password",
    "host": "localhost",
    "database": "furniture_store",
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
print("Connected to database.\n")

def parse_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")

def load_csv_auto(filename, table, date_columns=None):
    print(f"=== Загружаем {filename} → {table} ===")

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        placeholders = ", ".join(["%s"] * len(columns))
        col_names = ", ".join(columns)
        sql = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"

        count = 0
        for row in reader:
            values = []
            for col in columns:
                val = row[col] if row[col] != "" else None
                if date_columns and col in date_columns:
                    val = parse_date(val)
                values.append(val)

            try:
                cursor.execute(sql, tuple(values))
                count += 1
            except mysql.connector.IntegrityError as e:
                print(f"[FK ERROR] строка пропущена: {row}")
                print("Причина:", e)
            except Exception as e:
                print(f"[ERROR] строка пропущена: {row}")
                print("Причина:", e)

        db.commit()
        print(f"→ Загружено: {count} записей\n")

load_csv_auto("customers.csv", "customers")
load_csv_auto("products.csv", "products")
load_csv_auto("orders.csv", "orders", date_columns=["order_date", "ship_date"])
load_csv_auto("order_items.csv", "order_items")

cursor.close()
db.close()
print("\n=== Загрузка завершена успешно ===")
