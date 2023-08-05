import pexpect
import parsegrammar as gram

class Parser:

    def __init__(self, grammar):
        if isinstance(grammar, gram.Grammar):
            self.grammar = grammar
        else:
            raise ValueError(f'expected grammar.Grammar but got {type(grammar)}')

    def run(self):
        child = pexpect.spawn(self.grammar.getStart())
        patternList, stateList = self.grammar.getPossibleNext(self.grammar.getStart())
        while len(patternList) > 0 and len(stateList) > 0:
            try:
                index = child.expect(patternList)
                cur = stateList[index]
                patternList, stateList = self.grammar.getPossibleNext(cur)
                if self.grammar.isTerminal(cur):
                    break
                else:
                    child.sendline(cur)
            except pexpect.exceptions.TIMEOUT:
                child.close()
                print(f'Timeout Occured at: {cur}')
                return None
            except pexpect.exceptions.EOF:
                child.close(f'EOF Occured at: {cur}')
                print("")
                return None
        return child
        
        
