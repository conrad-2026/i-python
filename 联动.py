import json
import os

# 核心：操作本地JSON文件（替代TinyDB，无需安装任何库，Python自带支持）
class PingPongDB:
    def __init__(self, db_path="pingpong_db.json"):
        self.db_path = db_path
        # 若JSON文件不存在，自动创建并初始化结构
        if not os.path.exists(db_path):
            self.init_db()
    
    # 初始化JSON数据库结构（赛事表、选手表、成绩表）
    def init_db(self):
        init_data = {
            "event": [],  # 赛事表
            "player": [],  # 选手表
            "score": []    # 成绩表
        }
        self.save_data(init_data)
        print("JSON数据库初始化成功！已生成pingpong_db.json文件")
    
    # 读取JSON文件数据
    def read_data(self):
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # 保存数据到JSON文件
    def save_data(self, data):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    # 1. 添加赛事（对接manager.html的创建赛事功能）
    def add_event(self, event_name, event_time, event_addr, event_rule):
        data = self.read_data()
        data["event"].append({
            "event_name": event_name,
            "event_time": event_time,
            "event_addr": event_addr,
            "event_rule": event_rule
        })
        self.save_data(data)
        return True
    
    # 2. 添加选手（对接player.html的报名功能）
    def add_player(self, name, phone, event):
        data = self.read_data()
        # 避免重复报名（根据姓名+手机号判断）
        for player in data["player"]:
            if player["name"] == name and player["phone"] == phone:
                return False
        data["player"].append({
            "name": name,
            "phone": phone,
            "event": event,
            "join_time": "2026-05-10"  # 可后续修改为当前时间，简化版暂固定
        })
        self.save_data(data)
        return True
    
    # 3. 添加成绩（对接manager.html的成绩录入功能）
    def add_score(self, event_name, player_a, player_b, score, round):
        data = self.read_data()
        # 自动判断胜负（复刻开球网计分评定逻辑）
        score_a, score_b = map(int, score.split(":"))
        result = f"{player_a}获胜" if score_a > score_b else f"{player_b}获胜"
        data["score"].append({
            "event_name": event_name,
            "player_a": player_a,
            "player_b": player_b,
            "score": score,
            "round": round,
            "result": result
        })
        self.save_data(data)
        return True
    
    # 4. 查询选手成绩（对接player.html的成绩查询功能）
    def get_player_score(self, name):
        data = self.read_data()
        score_list = []
        for score in data["score"]:
            if score["player_a"] == name or score["player_b"] == name:
                opponent = score["player_b"] if score["player_a"] == name else score["player_a"]
                round_map = {
                    "group": "小组赛",
                    "quarter": "四分之一决赛",
                    "semi": "半决赛",
                    "final": "决赛"
                }
                score_list.append({
                    "match": f"{round_map.get(score['round'], '未知轮次')}第1场",
                    "opponent": opponent,
                    "score": score["score"],
                    "result": score["result"]
                })
        return score_list

# 测试脚本（运行后可验证功能，无需修改）
if __name__ == "__main__":
    db = PingPongDB()
    # 测试添加赛事
    db.add_event("2026年XX乒乓球公开赛", "2026-05-20", "XX体育馆", "单打7局4胜制，每局11分")
    # 测试添加选手
    db.add_player("张三", "13800138000", "single")
    # 测试添加成绩
    db.add_score("2026年XX乒乓球公开赛", "张三", "李四", "3:1", "group")
    # 测试查询成绩
    scores = db.get_player_score("张三")
    print("张三的成绩：", scores)
    print("所有功能测试完成！JSON数据库可正常使用，替代TinyDB实现数据联动")
    input()





    
