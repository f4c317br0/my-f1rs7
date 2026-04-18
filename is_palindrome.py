def is_palindrome(s):
    # Оставляем только буквы и приводим к нижнему регистру
    cleaned = ''.join(c.lower() for c in s if c.isalpha())
    
    def helper(left, right):
        if left >= right:
            return True
        if cleaned[left] != cleaned[right]:
            return False
        return helper(left + 1, right - 1)
    
    return helper(0, len(cleaned) - 1)
