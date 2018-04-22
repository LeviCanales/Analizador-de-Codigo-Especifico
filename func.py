def clean_code(all_txt, *args):
    for arg in args:
        all_txt = all_txt.replace(arg,' ')
    return all_txt