def truecolor_proc(r, g, b, char):
    return "\x1B[38;2;%d;%d;%dm%s\x1B[0m" % (r, g, b, char)
