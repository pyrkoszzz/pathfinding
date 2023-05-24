class StateAgent:
    def __init__(self, app_instance):
        self.app = app_instance
        self.states = self.app.config_agent.getStates()
        self.state = self.states['ready']
    
        