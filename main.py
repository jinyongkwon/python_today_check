from User.User import User

if __name__ == "__main__":
    print("이름을 입력하세요")
    name = input()
    user = User(name)
    user.run()
