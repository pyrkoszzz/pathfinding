class StateAgent:
    def __init__(self, app_instance):
        self.app = app_instance
        self.states = self.app.config_agent.getStates()
        self.state = None
        self.updateState("waiting")
        self.log = ""

    def canMazeBeSolved(self):
        return self.state == self.states['generated'] or self.state == self.states['solved']
    
    def canMazeBeExported(self):
        return self.state == self.states['generated'] or self.state == self.states['solved']
    
    def updateState(self, state_key):
        self.state = self.states[state_key]