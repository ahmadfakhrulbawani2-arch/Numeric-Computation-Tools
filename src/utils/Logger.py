import os
import logging

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.abspath(os.path.join(CURRENT_DIR, "../../activities.log"))

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)


def log_activities(action: str, status: str = "INFO") -> None:
    status = status.upper()
    if "ERROR" in status:
        logging.error(action)
    elif "WARNING" in status:
        logging.warning(action)
    else:
        logging.info(action)


def read_logs() -> None:
    if not os.path.exists(LOG_FILE):
        print("\033[93m[WARNING] Belum ada aktivitas yang tercatat di log.\033[0m")
        return

    try:
        cnt_err, cnt_info, cnt_warning = 0, 0, 0
        print("\n" + "=" * 20 + " RECENT HISTORY " + "=" * 20)
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if "ERROR" in line:
                    cnt_err += 1
                elif "WARNING" in line:
                    cnt_warning += 1
                elif "INFO" in line:
                    cnt_info += 1
                print(line.strip())
            print("\nTL;DR:")
            print(f"Total ERROR: {cnt_err}")
            print(f"Total WARNING: {cnt_warning}")
            print(f"Total INFO: {cnt_info}")
            print("=" * 57 + "\n")
    except Exception as e:
        print(f"\033[91m[ERROR] Gagal membaca file log: {e}\033[0m")
