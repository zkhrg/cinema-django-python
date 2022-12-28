from transliterate import translit
import os


def path_and_rename(path, title):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        edited_title = translit(title, 'uk', reversed=True)
        filename = f"{edited_title}.{ext}"

        return os.path.join(path, filename)
    return wrapper
