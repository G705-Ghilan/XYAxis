import sys

from rich.console import Console

console = Console()

# CharCode
C: list = [
    "│",
    "┌",
    "└",
    "┐",
    "┘",
    "─",
    "┼",
]

class XYPaint:
    def __init__(self, rang: range, text: str):
        self.controls = list(map(lambda i: (i, round(eval(text.replace("s", f"({i})")))), rang))
        console.print(str(self.controls)[1:-1].replace('),', ")\n\r").replace(" (", "(").replace('-', '[red]-[/red]'))
        __max = max([int(str(min(map(min, self.controls))).split('-', 1)[1]), max(map(max, self.controls))])
        self.line_rang = range(-__max, __max + 1)
        self.max = max(len(str(i)) for i in self.line_rang) 
        
            
        

    def center(self, text: str, max: int, tap=' ') -> str:
        text = str(text)
        text = tap*(max // 2 - len(text) // 2) + text
        return text + tap*(max - len(text))

    @property
    def paint_x(self) -> str:
        temp = list(self.line_rang)
        temp[len(temp)//2] = C[0]
        line_1 = f'≺{C[-2]*2}{(self.center(C[-1], self.max, C[-2]) + C[-2])*(len(temp))}{C[-2]*2}≻'
        line_2 = f"   {' '.join(self.center(i, self.max) for i in temp)}   "
        return f'{line_1}\n{line_2}'

    @property
    def paint_y(self) -> tuple:
        end = ' '*(self.max + 1)
        data = ['', '']
        t = 0
        for i in self.line_rang[::-1]:
            data[t] += (f"{' '*(self.max - len(str(i)))}{i}{C[-1]}" if i < 0 else f"{C[-1]}{i}{' '*(self.max - 1 - len(str(i)))}") + '\n'
            t += 1 if  i == 0 else 0 # ⋎][⋏
            
        return (
            data[0].rsplit('\n', 2)[0],
            data[1]
        )

    # (..., ...)
    def filter_controls(self, mode: int) -> list:
        data = []
        num = list(self.line_rang[self.line_rang.index(0):])[::-1]
        plus = lambda t: int(str(t).split('-')[-1])
        for i in self.controls:
            i = list(i)
            if i[0] < 0 and i[1] > 0 and mode == 1:
                a = int(str(i[0]).split('-')[-1])#plus[i[0]]
                data.append(([a*self.max + a - 1, num[i[1]]]))
            elif i[0] > 0 and i[1] > 0 and mode == 2:
                a = i[0]
                data.append([a if a == 1 else a*self.max + a - self.max, num[i[1]]])
            elif i[0] < 0 and i[1] < 0 and mode == 3:
                i = [plus(i[0]), plus(i[1])]
                data.append([i[0]*self.max + i[0] - self.max - 1, num[i[1]]])
            elif i[0] > 0 and i[1] < 0 and mode == 4:
                i[1] = plus(i[1])
                data.append([i[0]*self.max + i[0] - 1, num[i[1]]])
        return data

    @property
    def paint_box_1(self) -> list:
        y = self.paint_y[0]
        parts = []
        data = self.filter_controls(1)
        lines = []
        for i in range(len(self.line_rang) // 2):
            f = ''
            tap = " "
            for t in range((len(self.line_rang) - 1)*(self.max + 1) // 2)[::-1]:
                if [t, i] in data:
                    f += C[1]
                    tap = C[-2]
                    lines.append(t)
                else:
                    f += (tap if t not in lines else C[0])
            parts.append(f)
            
        return parts

    @property
    def paint_box_2(self) -> list:
        parts = []
        data = self.filter_controls(2)
        #print(data)
        lines = []
        for i in range(len(self.line_rang) // 2):
            f = ''
            tap = ' '
            for t in range((len(self.line_rang) - 1)*(self.max + 1) // 2)[::-1]:
                if [t, i] in data:
                    f += C[3]
                    lines.append(t)
                    tap = C[-2]
                else:
                    f += (C[0] if t in lines else tap)
            parts.append(f[::-1])
        return parts

    @property
    def paint_box_3(self) -> list:
        parts = []
        data = self.filter_controls(3)
        lines = []
        for i in range(len(self.line_rang) // 2):
            f = ''
            tap = ' '
            for t in range((len(self.line_rang) - 1)*(self.max + 1) // 2 - self.max)[::-1]:
                if [t, i] in data:
                    f += C[2]
                    lines.append(t)
                    tap = C[-2]
                else:
                    f += (C[0] if t in lines else tap)
            parts.append(f)
        return parts[::-1]
        
    @property
    def paint_box_4(self) -> list:
        parts = []
        data = self.filter_controls(4)
        lines = []
        for i in range(len(self.line_rang) // 2):
            f = ''
            tap = ' '
            for t in range((len(self.line_rang) - 1)*(self.max + 1) // 2)[::-1]:
                if [t, i] in data:
                    f += C[4]
                    lines.append(t)
                    tap = C[-2]
                else:
                    f += C[0] if t in lines else tap
            parts.append(f[::-1])
        return parts[::-1]


    def start(self):
        axis_x = self.paint_y
        output = '\n'.join(
            map(
                lambda t: '    ' + ''.join(t),
                zip(
                    self.paint_box_1,
                    axis_x[0].split('\n'),
                    self.paint_box_2
                )
            )
        ) + "\n" + (self.paint_x) + "\n"
        output += '\n'.join(
            map(
                lambda t: '    ' + ''.join(t),
                zip(
                    self.paint_box_3,
                    axis_x[1].split('\n'),
                    self.paint_box_4
                )
            )
        ) + "\n"
        tap = ' '*(len(output.split('\n')[0])//2+1)
        output = f"{tap}⋏\n{tap}{C[0]}\n{output}{tap}{C[0]}\n{tap}⋎".replace('-', "[red]-[/red]")
        
        console.print(output)
        
            
            
        
    
if __name__ == "__main__":
    try:
        argv = sys.argv
        paint = XYPaint(range(int(argv[-3]), int(argv[-2])), argv[-1])
        paint.start()
    except Exception as e:
        console.print(f'[red]{e.__class__.__name__}[/red]: {e}')
        console.print('example:\n  test -2 3 s**3\n  !"s" is range(-2, 3)')
