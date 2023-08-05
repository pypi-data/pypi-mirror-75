from time import sleep


def progress_bar(length: int,
                 bar: str = '#',
                 delay: (float, int) = 0.01,
                 **kwargs):
    try:
        flush = kwargs['flush']
    except KeyError:
        flush = True
    for i in range(1, length + 1):
        percent = round(i / length * 100)
        if flush:
            print('\r', f'{percent}% |{round(percent / 2) * bar}| {i}/{length}', end=' ', flush=flush)
        else:
            print(f'{percent}% |{round(percent / 2) * bar}| {i}/{length}', end='\n', flush=flush)
        sleep(delay)
    return None


if __name__ == '__main__':
    progress_bar(length=3141, delay=0.0001, bar='█')
