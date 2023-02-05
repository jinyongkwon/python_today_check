import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta


class FileHelper:
    def __init__(self, user_name):
        self.root_path = os.path.dirname(os.path.dirname(Path(__file__)))
        self.user_name_path = os.path.join(self.root_path, user_name)

    def create_user_dir(self, attr):
        user_attr_path = os.path.join(self.user_name_path, attr)
        if not os.path.exists(user_attr_path):
            os.makedirs(user_attr_path, exist_ok=True)

    def check_user_dir(self):
        if os.path.exists(self.user_name_path):
            user_attr_path = os.path.join(self.user_name_path, "Plan")
            if os.path.exists(user_attr_path):
                return "완료"
            else:
                return "계획"
        else:
            return "폴더"

    def make_csv(self, plan_list, attr):
        today = (datetime.utcnow() - timedelta(hours=9)).strftime("%Y%m%d")
        plan_df = pd.DataFrame(plan_list)
        user_attr_path = os.path.join(self.user_name_path, attr)
        plan_df.to_csv(os.path.join(user_attr_path, f"{today}_{attr}"))

    def read_csv(self, attr):
        user_attr_path = os.path.join(self.user_name_path, attr)
        plan_list = os.listdir(user_attr_path)
        plan_df = pd.read_csv(os.path.join(user_attr_path, max(plan_list)))
        if attr == 'Plan':
            return plan_df[["start_time", "end_time", "plan_name"]]
