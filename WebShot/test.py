
if __name__ == "__main__":
    with open('D:/Learning/pythonProject/WebShot/urls.txt', 'r') as f:
        config = f.readlines()
        weather_url = config[0]
        wehook_url = config[1]
        print(wehook_url)