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
                # Just to possibly separate out the timeout and EOF for future implementations
                raise
            except pexpect.exceptions.EOF:
                # Just to possibly separate out the timeout and EOF for future implementations
                raise
        return child
