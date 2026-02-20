import sys
import re
from argparse import ArgumentParser
from state.state import State

class StateGraph:
    """状態グラフを管理するクラスです
    """
    def __init__(self, str):
        str = str.replace('"', "'")
        self.states = self.parseState(str)
        self.parseTransition(self.states, str)
        self.states[self.parseSS(str)].ini = True

    def stateColoring(self):
        """状態に色付けするための情報を付加します。
        """
        # 状態から出ていくエッジが多い <-----------------------------> 状態に入るエッジが多い
        # 寒色系 <-------------------------------------------------------------------> 暖色系
        colorlist = ["#84b9cb", "#59b9c6", "#38b48b", "#69b076", "#b0ca71", "#dccb18", "#f8b500"]
        framelist = ["#007bbb", "#008899", "#006e54", "#007b43", "#7b8d42", "#928c36", "#f08300"]
        for st in self.states.values():
            if st.ini:
                st.fillColor = "#bbbcde"
                st.frameColor = "#3e62ad"
            elif len(st.trans) == 0:
                st.fillColor = "#f5b1aa"
                st.frameColor = "#e83929"
            else:
                diff = len(st.froms) - len(st.trans)
                if diff >= 3:
                    st.fillColor = colorlist[6]
                    st.frameColor = framelist[6]
                elif diff <= -3:
                    st.fillColor = colorlist[0]
                    st.frameColor = framelist[0]
                else:
                    st.fillColor = colorlist[diff + 3]
                    st.frameColor = framelist[diff + 3]
    
    def printDot(self):
        """状態グラフを DOT 言語の形式で標準出力に出力します。
        """
        print("digraph states {")
        print('node [style = "solid, filled", penwidth = "3"];')
        for st in self.states.values():
            for dst in st.trans:
                print('"', st.name, '"', "->", '"', dst.name, '"', ";")
            print('"', st.name, '"', '[color = "', st.frameColor, '", fillcolor = "', st.fillColor, '"];')
        print("}")

    @staticmethod
    def parseSS(str):
        """文字列を読み取って初期状態 (ss(ID,...) の形で表現される) の ID を取得します。

        Args:
            str (string): 入力文字列

        Returns:
            string: 初期状態の ID
        """
        return re.search("[0-9]+", re.search("ss\([0-9]+,", str).group(0)).group(0)
    
    @staticmethod
    def parseState(str):
        """文字列を読み取って状態と ID の組 (state(ID, name) の形で表される) を取得し、ID をキーとする辞書を返します

        Args:
            str (string): 入力文字列

        Returns:
            dictionary: ID をキーとし、値に State オブジェクトをもつ辞書
        """
        states = {}
        s = str
        # Find each "state(<id>," occurrence, then extract the brace-delimited body
        for m in re.finditer(r"state\(([0-9]+),", s):
            id = m.group(1)
            # locate the first '{' after the match
            start = s.find('{', m.end())
            if start == -1:
                continue
            # walk forward to find the matching '}' taking nesting into account
            i = start
            depth = 0
            end = -1
            while i < len(s):
                ch = s[i]
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
                i += 1
            if end == -1:
                # unmatched brace; skip this entry
                continue
            name = s[start:end+1]
            lastPos = 0
            # 状態に適宜改行を入れて読みやすくする
            while True:
                idx = name.find(' ', lastPos + 15)
                if idx == -1:
                    break
                lastPos = idx
                if lastPos + 1 < len(name) and name[lastPos + 1] != '}':
                    name = name[:lastPos] + '\n' + name[lastPos+1:]
            states[id] = State(name)
        return states

    @staticmethod
    def parseTransition(states, str):
        """文字列を読み取って遷移 ([遷移元 ID | 遷移先 ID] の形で表される) を取得し、状態の情報に遷移の情報を付加する

        Args:
            states (dictionary): ID をキーとし、値に State オブジェクトをもつ辞書
            str (string): 入力文字列
        """
        transition_group = re.findall("\[[0-9]+\|[0-9]+\]", str)
        for transition in transition_group:
            ts = re.findall("[0-9]+", transition)
            states[ts[0]].addTrans(states[ts[1]])
            states[ts[1]].addFroms(states[ts[0]])

def getOption():
    """実行時引数の設定をします

    Returns:
        ArgumentParser: 実行時引数の情報
    """
    argParser = ArgumentParser()
    argParser.add_argument("--colored", type = int, default = 1, help = "Colored or not (Default: 1)")
    argParser.add_argument("filename", type = str, nargs = "*", help = "Input file name")
    return argParser

if __name__ == "__main__":
    # main 部分
    parser = getOption()
    args = parser.parse_args()
    if len(args.filename) > 1:
        print("Too much args!")
        sys.exit()
    elif len(args.filename) == 1:
        with open(args.filename[0]) as f:
            str = f.read()
    elif len(args.filename) == 0:
        str = input()
    if args.colored:
        stateGraph = StateGraph(str)
        stateGraph.stateColoring()
        stateGraph.printDot()
    else:
        stateGraph = StateGraph(str)
        stateGraph.printDot()
