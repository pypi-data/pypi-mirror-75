from .color import truecolor_proc
default_tokens = {
    "@": 200,
    "#": 155,
    "&": 100,
    "*": 50,
    ".": 0
}

def default_rendition(img_slice, ascii_tokens):
    for char, threshold in ascii_tokens.items():
        if (img_slice.mean() >= threshold):
            return char

def truecolor_default(img_slice, ascii_tokens):
    char = default_rendition(img_slice, ascii_tokens)
    char = truecolor_proc(*img_slice.mean(axis=(1, 0)), char)
    return char

def colorwise_rendition(img_slice, ascii_tokens):
    for char, threshold in ascii_tokens.items():
        if (img_slice.max() >= threshold):
            return char

