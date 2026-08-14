import os
import csv
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "data.txt"
FREQ_HISTORY_FILE = BASE_DIR / "data" / "frequency_history.csv"


def load_loto7_data(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"未找到数据文件: {path}")

    with path.open("r", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f, delimiter="\t"))

    if not rows:
        raise ValueError("数据文件为空")

    records = []
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        if len(row) < 9:
            continue

        issue = row[0].strip()
        draw_date = row[1].strip()
        nums = [int(x.strip()) for x in row[2:9] if x.strip()]

        if len(nums) == 7:
            records.append({
                "issue": issue,
                "date": draw_date,
                "nums": nums
            })

    return records


def build_frequency_history(records):
    """
    计算每一期每个号码的累计出现频率，并保存为 CSV。
    """
    history_by_num = {n: [] for n in range(1, 38)}
    counts = Counter()

    history_rows = []
    for idx, record in enumerate(records, start=1):
        for n in record["nums"]:
            counts[n] += 1

        row = {
            "issue": record["issue"],
            "date": record["date"],
        }

        for n in range(1, 38):
            freq = counts[n] / idx
            row[str(n)] = round(freq, 6)
            history_by_num[n].append(freq)

        history_rows.append(row)

    # 保存频率历史
    with FREQ_HISTORY_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["issue", "date"] + [str(n) for n in range(1, 38)])
        writer.writeheader()
        writer.writerows(history_rows)

    return history_by_num


def compute_regression_scores(history_by_num, trim_count=10, alpha=0.5):
    """
    对每个号码：
    1. 取它的历史频率序列
    2. 去掉 10 个最大值和 10 个最小值
    3. 求去极值后的平均值
    4. 用最后一次值向平均值回归，算出一个期望值
    """
    results = []

    for n in range(1, 38):
        values = history_by_num[n]
        if not values:
            continue

        sorted_vals = sorted(values)
        if len(sorted_vals) > 2 * trim_count:
            trimmed = sorted_vals[trim_count:-trim_count]
        else:
            trimmed = sorted_vals

        avg = sum(trimmed) / len(trimmed) if trimmed else 0.0
        last_value = values[-1]

        # 回归到均值：last_value 向 avg 靠近
        expected = avg + (last_value - avg) * alpha

        results.append({
            "number": n,
            "expected": expected,
            "avg": avg,
            "last": last_value,
            "count": len(values),
        })

    results.sort(key=lambda x: x["expected"], reverse=True)
    return results


def main():
    records = load_loto7_data(DATA_FILE)
    history_by_num = build_frequency_history(records)
    results = compute_regression_scores(history_by_num)

    print("共分析期数:", len(records))
    print("频率历史文件已保存:", FREQ_HISTORY_FILE)

    print("\n按期望值排序的推荐号码：")
    for item in results[:15]:
        print(
            f"{item['number']:02d} | "
            f"期望={item['expected']:.6f} | "
            f"均值={item['avg']:.6f} | "
            f"最后一次={item['last']:.6f}"
        )


if __name__ == "__main__":
    main()