#!/usr/bin/env python3
"""
Pandoc Filter to remove all italic text (emph) from the document.
"""
import sys

from pandocfilters import toJSONFilter, Emph, Str, Para, Plain

def remove_italic(key, value, format_, meta):
    """
    Pandoc filter function that removes all Emph (italic) nodes.
    """
    if key == 'Emph':
        # 如果遇到 Emph 节点（即 \emph{} 或 \textit{}），递归处理其子节点
        # 并将所有子节点转换为普通文本（Str），从而去掉斜体
        # sys.stderr.write("remove_italic.py is being called!\n")
        print(f"Processing node: key={key}, value={value}")  # 调试输出
        new_children = []
        for child in value:
            if isinstance(child, dict):
                # 递归调用 remove_italic 处理子节点（虽然这里没有嵌套 Emph，但保留扩展性）
                filtered_child = remove_italic(key, child, format_, meta)
                if filtered_child:
                    new_children.append(filtered_child)
            else:
                # 如果子节点不是字典（比如直接是字符串），直接保留内容
                new_children.append(Str(child))
        # 返回一个 Plain 节点（而不是 Str），以保留段落结构
        return Plain(new_children)
    elif key == 'Math':
        # 如果是数学公式节点，直接返回原样（不处理斜体）
        sys.stderr.write("remove_italic.py is being called!2\n")
        return None
    # 其他情况不做处理
    sys.stderr.write("remove_italic.py is being called!\n")
    return None

if __name__ == "__main__":
    from pandocfilters import toJSONFilter
    toJSONFilter(remove_italic)