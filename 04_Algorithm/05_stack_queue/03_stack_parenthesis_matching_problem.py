def check_match(expression):
    # 스택
    stack = []
    # 여는 괄호라면?
    # 닫는 괄호라면?
    target = {
        ')': '(',
        '}': '{',
        ']': '['
    }
    # 모든 단어에 대해서 검사를 수행
    for char in expression:
        # 여는 괄호야?
        # if char in '([{':
        # dict get 메서드는 찾는키가 없으면 None
        open = target.get(char) # '(' .. or None
        if open is not None:    # 닫힌 괄호라면
            # 스택이 비어있지 않고
            if not stack or stack[-1] != open:
                return False
            # 닫는괄호랑 여는괄호가 일치하네?
            stack.pop()
        # elif char == '(' or char == '[' or char == '{'
        elif char in target.values():
            stack.append(char)
    # T/F
    # 스택이 비어있으면 True 아니면, False
    return not stack

# 예시
examples = ["(a(b)", "a(b)c)", "a{b(c[d]e}f)"]
for ex in examples:
    if check_match(ex): 
        print(f"{ex} 는 올바른 괄호") 
    else:
        print(f"{ex} 는 올바르지 않은 괄호")  
