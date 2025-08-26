def is_likely_source_code(data):
    """
    Checks if data looks like C/C++ source code
    """
    try:
        text = data.decode('utf-8', errors='ignore')
        
        cpp_keywords = [
            '#include', 'int main(', 'void main(', 'class ', 'struct ',
            'namespace ', 'template<', 'typedef ', '#define', '#ifdef',
            '#ifndef', '#pragma', 'public:', 'private:', 'protected:'
        ]
        
        for keyword in cpp_keywords:
            if keyword in text:
                return True
                
        if ('{' in text and '}' in text) or ('(' in text and ')' in text):
            printable_count = sum(1 for c in text if c.isprintable() or c.isspace())
            if printable_count / len(text) > 0.8:  # If more than 80% characters are printable
                return True
                
    except:
        pass
        
    return False
