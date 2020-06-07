
def normalize_text(text):
        upper_text = text.upper()

        replacements = (
            ("Á", "A"),
            ("É", "E"),
            ("Í", "I"),
            ("Ó", "O"),
            ("Ú", "U"),
        )
    
        for a, b in replacements:
            upper_text = upper_text.replace(a, b).replace(a.upper(), b.upper())
        return upper_text
