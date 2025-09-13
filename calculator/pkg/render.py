def render(expression, result):
    
    if isinstance(result, Exception):
        result_str = "Error"

    else:
        if isinstance(result, float):
            if result.is_integer():
                result_str = str(int(result))  # 5.0 -> "5"
            else:
                result_str = str(result)
        else:
            result_str = str(result)

    box_width = max(len(expression), len(result_str)) + 4

    box = []
    box.append("┌" + "─" * box_width + "┐")
    box.append(
        "│" + " " * 2 + expression + " " * (box_width - len(expression) - 2) + "│"
    )
    box.append("│" + " " * box_width + "│")
    box.append("│" + " " * 2 + "=" + " " * (box_width - 3) + "│")
    box.append("│" + " " * box_width + "│")
    box.append(
        "│" + " " * 2 + result_str + " " * (box_width - len(result_str) - 2) + "│"
    )
    box.append("└" + "─" * box_width + "┘")
    return "\n".join(box)