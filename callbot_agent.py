from pokerface import PokerPlayer

class CallbotAgent(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
    
    def act(self):
        if self.can_check_call():
            self.check_call()
            print("Callbot:\t\t calls")

        else:
            if self.can_fold():
                self.fold()
                print("Callbot:\t\t folds")
