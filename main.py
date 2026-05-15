import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs.json")


def load_logs():
    """logs.json を読み込んでリストで返す。なければ空リスト。"""
    if not LOG_FILE.exists():
        return []
    try:
        with LOG_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # 壊れたとき用の簡単な防御
        print("ログファイルの形式がおかしいため、空の状態から始めます。")
        return []

2
def save_logs(logs):
    """ログのリストを logs.json に保存する。"""
    with LOG_FILE.open("w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def add_log():
    """学習ログを1件追加する。"""
    print("\n=== 学習ログの追加 ===")
    topic = input("科目・トピックを入力してください（例: Python, SQL）: ").strip()
    detail = input("学習内容のメモを入力してください: ").strip()
    minutes_str = input("学習時間（分）を入力してください: ").strip()

    # 入力チェック（最低限）
    if not topic or not detail or not minutes_str.isdigit():
        print("入力値が正しくありません。やり直してください。")
        return

    minutes = int(minutes_str)
    today = datetime.now().strftime("%Y-%m-%d")

    logs = load_logs()
    logs.append(
        {
            "date": today,
            "topic": topic,
            "detail": detail,
            "minutes": minutes,
        }
    )
    save_logs(logs)
    print("学習ログを保存しました。")


def list_logs():
    """すべての学習ログを表示する。"""
    print("\n=== 学習ログ一覧 ===")
    logs = load_logs()
    if not logs:
        print("まだ学習ログがありません。")
        return

    for i, log in enumerate(logs, start=1):
        print(f"{i}. [{log['date']}] {log['topic']} ({log['minutes']}分)")
        print(f"   {log['detail']}")


def search_by_topic():
    """科目・トピックでログを検索する。"""
    print("\n=== 科目で検索 ===")
    keyword = input("検索したい科目・トピックを入力してください: ").strip()
    if not keyword:
        print("入力が空です。")
        return

    logs = load_logs()
    results = [log for log in logs if keyword.lower() in log["topic"].lower()]

    if not results:
        print("該当するログはありませんでした。")
        return

    for i, log in enumerate(results, start=1):
        print(f"{i}. [{log['date']}] {log['topic']} ({log['minutes']}分)")
        print(f"   {log['detail']}")


def show_total_last_7_days():
    """直近7日間の学習時間合計を表示する。"""
    print("\n=== 直近7日間の学習時間 ===")
    logs = load_logs()
    if not logs:
        print("まだ学習ログがありません。")
        return

    today = datetime.now().date()
    total = 0

    for log in logs:
        try:
            d = datetime.strptime(log["date"], "%Y-%m-%d").date()
        except ValueError:
            continue
        if (today - d).days <= 7:
            total += log.get("minutes", 0)

    print(f"直近7日間の合計学習時間: {total} 分")


def main():
    while True:
        print("\n=== 学習ログCLI ===")
        print("1. 学習ログを追加する")
        print("2. 学習ログを一覧表示する")
        print("3. 科目で検索する")
        print("4. 直近7日間の学習時間を表示する")
        print("5. 終了する")

        choice = input("番号を入力してください: ").strip()

        if choice == "1":
            add_log()
        elif choice == "2":
            list_logs()
        elif choice == "3":
            search_by_topic()
        elif choice == "4":
            show_total_last_7_days()
        elif choice == "5":
            print("終了します。")
            break
        else:
            print("1〜5の番号で入力してください。")


if __name__ == "__main__":
    main()