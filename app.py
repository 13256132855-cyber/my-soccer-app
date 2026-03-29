import os
import re
import zipfile

target_files = ["bodan2.xlsx", "bodan3.xlsx", "bodan4.xlsx"]


def ultra_scan_5d(file_path):
    """【5维解析】抓取 1:0, 1:1, 1:2, 0:1, 0:2 五个核心比分赔率"""
    results = []
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            strings = []
            if "xl/sharedStrings.xml" in z.namelist():
                with z.open("xl/sharedStrings.xml") as f:
                    str_content = f.read().decode("utf-8")
                    strings = re.findall(r"<t>(.*?)</t>", str_content)

            with z.open("xl/worksheets/sheet1.xml") as f:
                content = f.read().decode("utf-8")
                rows = re.findall(r"<row.*?>(.*?)</row>", content)

                for row in rows:
                    c_vals = re.findall(r"<v>(.*?)</v>", row)
                    if len(c_vals) < 7:
                        continue

                    floats = []
                    text_pieces = []

                    for v in c_vals:
                        try:
                            val = float(v)
                            if val.is_integer() and 0 <= int(val) < len(strings):
                                text_pieces.append(strings[int(val)])
                            elif 1.0 < val < 100.0:
                                floats.append(val)
                        except:
                            continue

                    # 提取前 5 个赔率作为 5维特征向量
                    if len(floats) >= 5:
                        results.append({"odds": floats[:5], "texts": text_pieces})
    except Exception as e:
        pass
    return results


def run_5d_mirror():
    possible_dirs = [
        "/sdcard/Download/",
        "/storage/emulated/0/Download/",
        "/storage/emulated/0/Downloads/",
    ]
    valid_paths = []
    print("🔎 正在全自动搜寻您的 3 个表格文件...")
    for filename in target_files:
        for directory in possible_dirs:
            full_path = os.path.join(directory, filename)
            if os.path.exists(full_path):
                print(f"🎯 成功找到文件: {full_path}")
                valid_paths.append(full_path)
                break

    if not valid_paths:
        print("❌ 下载目录里一个表格都没找到！")
        return

    print("\n=== 🎯 5维波胆历史操盘镜像系统 ===")
    try:
        q10 = float(input("请输入今日【1:0】赔率: "))
        q11 = float(input("请输入今日【1:1】赔率: "))
        q12 = float(input("请输入今日【1:2】赔率: "))
        q01 = float(input("请输入今日【0:1】赔率: "))
        q02 = float(input("请输入今日【0:2】赔率: "))
    except:
        print("❌ 输入有误，请输入纯数字。")
        return

    print("\n📂 正在开启【极速雷达模式】读取数据，请稍候...")
    db_entries = []
    for path in valid_paths:
        vectors = ultra_scan_5d(path)
        for item in vectors:
            db_entries.append(
                {
                    "vector": item["odds"],
                    "texts": item["texts"],
                    "file": os.path.basename(path),
                }
            )

    print(f"✅ 成功穿透抓取了 {len(db_entries)} 组带赛果的赔率特征！")

    # 计算 5维 欧氏距离
    results = []
    for entry in db_entries:
        dist = (
            (q10 - entry["vector"][0]) ** 2
            + (q11 - entry["vector"][1]) ** 2
            + (q12 - entry["vector"][2]) ** 2
            + (q01 - entry["vector"][3]) ** 2
            + (q02 - entry["vector"][4]) ** 2
        ) ** 0.5
        results.append((dist, entry))

    results.sort(key=lambda x: x[0])

    print("\n📊 【高度相似历史镜像复盘】")
    for i in range(min(3, len(results))):
        dist, entry = results[i]
        sim = max(0, 100 - dist * 3)  # 5维空间距离拉大，调整下系数
        h_odds = entry["vector"]
        texts = entry["texts"]

        date_str = "未知日期"
        league = "未知联赛"
        match_info = []

        for t in texts:
            if "周" in t or re.search(r"\d{4}-\d{2}-\d{2}", t):
                date_str = t
            elif "杯" in t or "联赛" in t or "甲" in t:
                league = t
            elif "*" in t or ":" in t:
                match_info.append(t)

        print(f"\n" + "=" * 30)
        print(f"🔥 镜像 {i+1} [相似度: {sim:.1f}%]")
        print("=" * 30)
        print(f" 📅 比赛时间: {date_str}")
        print(f" 🏆 所属联赛: {league}")
        print(f" 📊 历史比分参考: {' / '.join(match_info) if match_info else '无'}")
        print(f" 📂 来源表格: [{entry['file']}]")
        print("-" * 30)
        print(" 📈 历史5项赔率:")
        print(
            f"    [1:0]->{h_odds[0]} | [1:1]->{h_odds[1]} | [1:2]->{h_odds[2]}"
        )
        print(f"    [0:1]->{h_odds[3]} | [0:2]->{h_odds[4]}")
        print("-" * 30)
        print(" 📝 完整抓取文本片段:")
        for piece in texts[:5]:
            print(f"    • {piece}")


if __name__ == "__main__":
    run_5d_mirror()
