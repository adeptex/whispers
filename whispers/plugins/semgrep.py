from itertools import zip_longest
from json import loads as json_loads
from logging import debug
from pathlib import Path
from subprocess import check_output
from typing import Any, Dict, Iterable, List, Tuple

from whispers.core.constants import MAP_AST_LANG, REGEX_AST_FILE_VERSION
from whispers.core.utils import global_exception_handler
from whispers.models.pair import KeyValuePair


class AST:
    ARG = "Arg"
    ARGKWD = "ArgKwd"
    ARRAYACCESS = "ArrayAccess"
    ASSIGN = "Assign"
    ASSIGNOP = "AssignOp"
    ATOM = "Atom"
    CALL = "Call"
    CONDITIONAL = "Conditional"
    CONTAINER = "Container"
    DEFSTMT = "DefStmt"
    DOTACCESS = "DotAccess"
    EN = "EN"
    EQ = "Eq"
    FIELDDEFCOLON = "FieldDefColon"
    FN = "FN"
    ID = "Id"
    IDSPECIAL = "IdSpecial"
    L = "L"
    N = "N"
    NAME = "name"
    NOTEQ = "NotEq"
    OP = "Op"
    OR = "Or"
    SOME = "some"
    STRING = "String"
    TUPLE = "Tuple"
    TYPEDEF = "TypeDef"
    VARDEF = "VarDef"
    VINIT = "vinit"

    @staticmethod
    def language(filepath: str) -> str:
        """Converts file extension to a Semgrep-supported language"""
        ext = filepath.split(".")[-1].lower()
        lang = REGEX_AST_FILE_VERSION.sub("", ext)
        return MAP_AST_LANG.get(lang, lang)

    @staticmethod
    def dump(filepath: str) -> str:
        """Dump AST using Semgrep"""
        argv = [
            "semgrep",
            "scan",
            "--experimental",
            "--metrics=off",
            "--quiet",
            "--dump-ast",
            "--json",
            f"--lang={AST.language(filepath)}",
            filepath,
        ]

        debug(f"{__name__}.AST.dump: {' '.join(argv)}")

        try:
            return check_output(argv).decode()

        except Exception:
            global_exception_handler(filepath)
            return "{}"

    @staticmethod
    def name(ast: Dict) -> str:
        tree = ast.get(AST.N, {}) or ast.get(AST.EN, {}) or ast.get(AST.FN, {})
        if not tree:
            return ""

        return tree.get(AST.ID, [[""]])[0][0]

    @staticmethod
    def literal(ast: Dict) -> str:
        ast_L = ast.get(AST.L, {})
        return ast_L.get(AST.STRING, [""])[0] or ast_L.get(AST.ATOM, ["", [""]])[1][0]

    @staticmethod
    def call_op(ast: List) -> str:
        idspecial = ast[0].get(AST.IDSPECIAL, [{}])[0]
        if isinstance(idspecial, str):
            return ""

        return idspecial.get(AST.OP, "")

    @staticmethod
    def call_arg(ast: Dict) -> str:
        arg = ast.get(AST.CALL, [{}, [{}]])[1][0].get(AST.ARG, {})
        return AST.literal(arg) or AST.name(arg)

    @staticmethod
    def call_args(ast: List, key: str = "", value: str = "") -> Tuple[str, str]:
        for arg in ast:
            arg = arg.get(AST.ARG, {})

            if AST.CALL in arg:
                key, value = AST.call_args(arg[AST.CALL][1], key, value)

            if not key and any([name in arg for name in [AST.N, AST.EN, AST.FN]]):
                key = AST.name(arg)

            if not value and AST.L in arg:
                value = AST.literal(arg)

        return key, value

    @staticmethod
    def call_kwargs(ast: List) -> Tuple[str, str]:
        key = ast[0][0]
        value = AST.literal(ast[1])
        return key, value

    @staticmethod
    def call(ast: List, key: str = "", value: str = "") -> Iterable[Tuple[str, str]]:
        func = ast[0]
        args = ast[1]

        if AST.DOTACCESS in func and len(args):
            name = func[AST.DOTACCESS][0]
            key = AST.literal(name) or AST.name(name)
            value = AST.literal(args[0].get(AST.ARG, {}))

        if len(args) >= 2:
            call_arg_1 = args[0].get(AST.ARG, {})
            call_arg_2 = args[1].get(AST.ARG, {})

            key = AST.literal(call_arg_1)

            if AST.CONDITIONAL in call_arg_2:
                value = AST.literal(call_arg_2[AST.CONDITIONAL][-1])

            else:
                value = AST.literal(call_arg_2)

        return key, value

    @staticmethod
    def dotaccess(ast: List) -> str:
        tree = ast[0][AST.DOTACCESS][-1]
        return AST.name(tree)

    @staticmethod
    def defstmt(ast: List) -> Tuple[str, str]:
        name = ast[0].get(AST.NAME, {})
        key = AST.name(name)

        vardef = ast[1].get(AST.VARDEF, {}) or ast[1].get(AST.FIELDDEFCOLON, {})
        vinit = vardef.get(AST.VINIT, {}) or {}
        some = vinit.get(AST.SOME, {})

        if AST.CALL in some:
            if AST.DOTACCESS in some[AST.CALL][0]:
                key = AST.dotaccess(some[AST.CALL])

            elif AST.IDSPECIAL in some[AST.CALL][0]:
                value = AST.literal(some[AST.CALL][1][-1].get(AST.ARG, {}))
                return key, value

            key = AST.name(some[AST.CALL][0])
            value = AST.call_args(some[AST.CALL][1])[1]

        else:
            value = AST.literal(some)

        return key, value

    @staticmethod
    def assign(ast: List, key: str = "", value: str = "") -> Tuple[str, str]:
        if AST.ARRAYACCESS in ast[0]:
            tree = ast[0][AST.ARRAYACCESS][-1]
            key = AST.name(tree) or AST.literal(tree)

        elif AST.DOTACCESS in ast[0]:
            key = AST.dotaccess(ast)

        elif AST.CALL in ast[0]:
            key = AST.call_arg(ast[0])

        else:
            key = AST.name(ast[0])

        if AST.CALL in ast[2]:
            call_ast = ast[2][AST.CALL]

            if AST.DOTACCESS in call_ast[0]:
                value = AST.literal(call_ast[1][0].get(AST.ARG, {}))

            elif AST.call_op(call_ast) == AST.OR:
                value = AST.literal(call_ast[1][-1].get(AST.ARG, {}))

        else:
            value = AST.literal(ast[2])

        return key, value

    @staticmethod
    def assignop(ast: List) -> Iterable[Tuple[str, str]]:
        if AST.CONTAINER in ast[0]:
            keys_list = ast[0].get(AST.CONTAINER, [AST.TUPLE, []])[1]
        else:
            keys_list = [ast[0]]

        if AST.CONTAINER in ast[2]:
            values_list = ast[2].get(AST.CONTAINER, [AST.TUPLE, []])[1]
        else:
            values_list = [ast[2]]

        keys = list(map(lambda key: AST.name(key), keys_list))
        values = list(map(lambda value: AST.literal(value), values_list))
        pairs = zip_longest(keys, values, fillvalue=values[0])
        yield from pairs


class Semgrep:
    def pairs(self, filepath: Path) -> Iterable[KeyValuePair]:
        ast = json_loads(AST.dump(filepath.as_posix()))
        pairs = filter(lambda pair: pair.key and pair.value, self.traverse(ast))
        yield from pairs

    def traverse(self, ast: Any) -> Iterable[KeyValuePair]:
        """Recursively traverse AST yielding pairs"""
        if isinstance(ast, dict):
            for ast_key, ast_values in ast.items():
                if ast_key == AST.ASSIGN:
                    key, value = AST.assign(ast_values)
                    yield KeyValuePair(key, value)

                elif ast_key == AST.ASSIGNOP:
                    pairs = AST.assignop(ast_values)
                    yield from map(lambda pair: KeyValuePair(*pair), pairs)
                    return StopIteration

                elif ast_key == AST.DEFSTMT:
                    key, value = AST.defstmt(ast_values)
                    yield KeyValuePair(key, value)

                elif ast_key == AST.CONTAINER and AST.TUPLE in ast_values:
                    key = AST.literal(ast_values[1][0])
                    value = AST.literal(ast_values[1][1])
                    yield KeyValuePair(key, value)
                    return StopIteration

                elif ast_key == AST.CALL:
                    key, value = AST.call(ast_values)
                    yield KeyValuePair(key, value)

                    if AST.call_op(ast_values) in [AST.EQ, AST.NOTEQ]:
                        key, value = AST.call_args(ast_values[1])
                        yield KeyValuePair(key, value)
                        return StopIteration

                elif ast_key == AST.ARGKWD and len(ast_values) > 1:
                    key, value = AST.call_kwargs(ast_values)
                    yield KeyValuePair(key, value)
                    return StopIteration

                yield from self.traverse(ast_values)

        elif isinstance(ast, list):
            for item in ast:
                yield from self.traverse(item)

        return StopIteration
