import numpy as np
import matplotlib.pyplot as plot
import time

class Equation:
    def __init__(self, eq):
        self.eq = eq
    def value_at(self, at):
        string = ''
        for char in self.eq:
            if char == 'x':
                string += f'{at}'
            else:
                string += char
        to_eval = string
        for char in to_eval:
            if char.isalpha():
                raise GraphingError.HostileAttackError
        code = compile(to_eval, 'string', 'eval')
        result = eval(code)
        return result

class GraphingError(Exception):
    def __str__(self):
        return 'General Graphing Error Received'
    class HostileAttackError(Exception):
        def __str__(self):
            return 'Hostile Attack Detected'
    class InstanceError(Exception):
        def __init__(self, t):
            self.t = t
        def __str__(self):
            return f'Wrong Instance Entered, Expected {self.t}'

class Grapher:
    async def graph(eq, timetoclose=None):
        if not isinstance(eq, Equation):
            raise GraphingError.InstanceError(Equation)
        x = np.array(range(-100,100))
        y = []
        for i in range(-100, 100):
            y.append(eq.value_at(i))
        plot.plot(x, y)
        plot.show()
        await waitclose(plot, timetoclose)
    async def waitclose(plot, time):
        if time == None:
            return
        t = 0
        while t != timetoclose:
            time.sleep(1)
            t += 1
        plot.close()
        return
