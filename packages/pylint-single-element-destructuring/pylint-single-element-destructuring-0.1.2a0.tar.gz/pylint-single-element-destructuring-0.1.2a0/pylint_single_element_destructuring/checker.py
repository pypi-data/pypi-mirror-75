from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker


class SingleElementDestructuring(BaseChecker):
    __implements__ = IAstroidChecker

    name = "single-element-destructuring-checker"

    SINGLE_ELEMENT_DESTRUCTURING_MSG = "single-element-destructuring"
    msgs = {
        "W0001": (
            "Uses single element destructuring",
            SINGLE_ELEMENT_DESTRUCTURING_MSG,
            "Single element destructuring should not be used.",
        ),
    }
    options = (
        (
            "ignore-single-element-list-destructuring",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Allow destructuring using lists, e.g [x] = [10]",
            },
        ),
    )

    priority = -1

    def visit_assign(self, node):
        if not hasattr(node, "targets"):
            return
        not_allowed_lhs = ["builtins.tuple"]
        if not self.config.ignore_single_element_list_destructuring:
            not_allowed_lhs.append("builtins.list")
        for target in node.targets:
            if hasattr(target, "pytype") and target.pytype() in not_allowed_lhs:
                if len(list(target.get_children())) == 1:
                    self.add_message(self.SINGLE_ELEMENT_DESTRUCTURING_MSG, node=node)


def register(linter):
    linter.register_checker(SingleElementDestructuring(linter))
