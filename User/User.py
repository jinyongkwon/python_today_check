from datetime import datetime, timedelta
from Helper.FileHelper import FileHelper


class User:
    def __init__(self, name):
        self.name: str = name
        self.file: FileHelper = FileHelper(name)

    def run(self):
        self.user_plan_check()
        plan_df = self.file.read_csv("Plan")
        point = self.today_check(plan_df)
        today = (datetime.utcnow() - timedelta(hours=9)).strftime("%Y%m%d")
        check_dict = {"date": [today], "score": [point]}
        self.file.create_user_dir("Check")
        self.file.make_csv(check_dict, "Check")

    def today_check(self, plan_df):
        point = 0
        success_point = 100 / len(plan_df)
        for i in range(len(plan_df)):
            start_time = plan_df.loc[i, "start_time"]
            end_time = plan_df.loc[i, "end_time"]
            plan_name = plan_df.loc[i, "plan_name"]
            print(f"{start_time} ~ {end_time} 동안 {plan_name}을(를) 하였습니까??")
            print(f"했으면 O, 안했으면 X를 입력해주세요")
            while True:
                check = input()
                if check == "X" or check == "x":
                    print(
                        "다른 무언가 의미있는 일을 하였는가요? \n계획한 일이 아닌 다른일에 대한 점수를 매겨주세요(숫자만 입력)")
                    print(f"최대점수는 {int(success_point)}입니다.")
                    while True:
                        self_point = input()
                        if not self_point.isnumeric() or int(self_point) > int(success_point):
                            print("숫자를 입력하지 않으셨거나, 최대점수를 넘은 점수를 입력하였습니다.")
                        else:
                            point += int(self_point)
                            break
                    break
                elif check == "O" or check == "o":
                    point += success_point
                    break
                else:
                    print("O또는 X만 입력해주세요")
        print(f"오늘 하루 당신의 점수는 {int(point)}점 입니다. \n오늘 하루도 수고하셨습니다.")
        return int(point)

    def user_plan_check(self):
        check = self.file.check_user_dir()
        if check != "완료":
            self.file.create_user_dir("Plan")
        else:
            plan_list = self.start_plan()
            self.file.make_csv(plan_list, "Plan")
        if self.set_process() == 1 :
            plan_list = self.start_plan()
            self.file.make_csv(plan_list, "Plan")

    def set_process(self):
        print("계획을 다시 작성할려면 1번을 눌러주시고 \n오늘 하루를 확인하시려면 2번을 눌러주세요")
        while True:
            num = input()
            if num.isnumeric() and (num == "1" or num == "2"):
                break
            else:
                print("1또는 2만 입력해주세요")
        return int(num)

    def start_plan(self):
        print("계획을 입력해주세요")
        print("모든 계획이 끝나면 0이나 끝을 입력해주세요")
        print("주의! 아래 예시와 같은포맷으로 입력해야 하며, 24시간을 기준으로 입력하세요")
        print("ex)12:00 ~ 13:00 운동")
        plan_list = {
            'start_time': [],
            'end_time': [],
            'plan_name': [],
        }
        while True:
            text = input()
            if text == "0" or text == "끝":
                break
            try:
                text = text.split()
                if ":" in text[0]:
                    plan_list['start_time'].append(text[0])
                else:
                    raise Exception("시간이 아닙니다.")
                plan_list['end_time'].append(text[2])
                plan_list['plan_name'].append(" ".join(text[3:]))
            except (Exception):
                print("포맷에 맞게 입력해주세요!")
        return plan_list
