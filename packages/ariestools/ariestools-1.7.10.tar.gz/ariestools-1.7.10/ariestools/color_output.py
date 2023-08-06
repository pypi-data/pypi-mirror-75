import hues

ANSIColors = [
    'black', 'red', 'green', 'yellow',
    'blue', 'magenta', 'cyan', 'white',
]


def black(*msg, sep=' ', end='\n'):
    print(hues.huestr(" ".join([str(i) for i in msg])).black.colorized, sep=sep, end=end)


def red(*msg, sep=' ', end='\n'):
    print(hues.huestr(" ".join([str(i) for i in msg])).red.colorized,  sep=sep, end=end)


def green(*msg, sep=' ', end='\n'):
    print(hues.huestr(" ".join([str(i) for i in msg])).green.colorized,  sep=sep, end=end)


def yellow(*msg, sep=' ', end='\n'):
    print(hues.huestr(" ".join([str(i) for i in msg])).yellow.colorized,  sep=sep, end=end)


def blue(*msg, sep=' ', end='\n'):
    print(hues.huestr(" ".join([str(i) for i in msg])).blue.colorized,  sep=sep, end=end)


def magenta(*msg, sep=' ', end='\n'):
    print(hues.huestr(" ".join([str(i) for i in msg])).magenta.colorized, sep=sep,  end=end)


def cyan(*msg, sep=' ', end='\n'):
    print(hues.huestr(" ".join([str(i) for i in msg])).cyan.colorized,  sep=sep, end=end)


def white(*msg, sep=' ', end='\n'):
    print(hues.huestr(" ".join([str(i) for i in msg])).white.colorized, sep=sep,  end=end)
