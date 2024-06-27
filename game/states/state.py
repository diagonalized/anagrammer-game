# stack implementation of a state manager
class State():
    def __init__(self, game):
        # reference to game object
        self.game = game
        # TODO: back button
        self.previous_state = None

    def update(self, delta_time, actions):
        # TODO: input handling
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        # check if there is a previous state
        if len(self.game.state_stack) > 1:
            self.previous_state = self.game.state_stack[-1]

        # add current state to stack
        self.game.state_stack.append(self)

    def exit_state(self):
        # remove current state from stack
        self.game.state_stack.pop()
