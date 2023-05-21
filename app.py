import helper

class App:
    def __init__(self):
        self.running = True
        self.config = helper.loadConfig()

if __name__ == "__main__":
    app = App()
    print(app.config)  