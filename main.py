# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


from operator import itemgetter


COMMON_MONITORS = [
    ((7680, 2160), (57,)),
    ((5120, 2880), (27,)),
    ((5120, 2160), (45, 40, 34)),
    ((5120, 1440), (49,)),
    ((3840, 2560), (28, 27,)),
    ((3840, 2160), (27, 28, 32, 37, 40, 41.5, 42.51, 43, 48, 49,)),
    ((3840, 1600), (37.5, 38, 48,)),
    ((3440, 1440), (34, 35,)),
    ((2560, 2880), (28,)),
    ((2560, 1600), (30, 24,)),
    ((2560, 1440), (25, 27, 32,)),
    ((2560, 1080), (26, 29, 30, 34,)),
    ((1920, 1200), (24, 32,)),
    ((1920, 1080), (20, 21.5, 23, 24, 27, 32,)),
]


class Resolution:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @property
    def ratio(self):
        return self.width / self.height


class Monitor:

    def __init__(self, resolution: Resolution, size: float):
        self.size = size
        self.resolution = resolution

    def __repr__(self):
        line = ' | '.join([
            f'SIZE: {self.size:05.02f}',
            f'PIXEL: {self.resolution.width:4d}x{self.resolution.height:4d}',
            f'DPI: {self.dpi:07.03f}',
        ])
        return f'| {line} |'

    def __sub__(self, monitor):
        return self.dpi - monitor.dpi

    @property
    def dpi(self):
        return pow(self.resolution.width ** 2 + self.resolution.height ** 2, 0.5) / self.size

    def compare(self, monitors, sort=True, limit=None, delta_limit=None):
        print('{}        REFERENCE |'.format(self))
        print('|:-----------:|:----------------:|:------------:|:----------------:|')
        # print('|:----------------:|:-----------:|:------------:|:----------------:|')
        compared = [(v, abs(self - v)) for v in monitors.values() if v != self]
        if sort:
            compared = sorted(compared, key=itemgetter(1))
        if limit:
            compared = compared[:limit]
        if delta_limit:
            compared = [v for v in compared if v[-1] <= delta_limit]

        for v, delta in compared:
            print('{} DELTA: {:06.03f}dpi |'.format(v, delta))
        # print('-' * 68)
        print()
        return compared


class Monitors:
    def __init__(self, monitors):
        self.monitors = {}
        for resolution, sizes in COMMON_MONITORS:
            for size in sizes:
                key = '{}-{}x{}'.format(size, *resolution)
                value = Monitor(Resolution(*resolution), size)
                self.monitors.update({key: value})

    def get(self, size, resolution) -> Monitor:
        key = '{}-{}x{}'.format(size, *resolution)
        return self.monitors.get(key)

    def compare(self, size, resolution,
                sort=True, limit=None, delta_limit=None):
        monitor = self.get(size, resolution)
        return monitor.compare(
            self.monitors, sort=sort, limit=limit, delta_limit=delta_limit)


monitors = Monitors(COMMON_MONITORS)


if __name__ == '__main__':
    limit = 20
    delta_limit = 5.0
    monitors.compare(20, (1920, 1080), limit=limit, delta_limit=delta_limit)
    monitors.compare(21.5, (1920, 1080), limit=limit, delta_limit=delta_limit)
    monitors.compare(23, (1920, 1080), limit=limit, delta_limit=delta_limit)
    monitors.compare(24, (1920, 1080), limit=limit, delta_limit=delta_limit)
    monitors.compare(25, (2560, 1440), limit=limit, delta_limit=delta_limit)
    monitors.compare(27, (1920, 1080), limit=limit, delta_limit=delta_limit)
    monitors.compare(27, (2560, 1440), limit=limit, delta_limit=delta_limit)
    monitors.compare(30, (2560, 1600), limit=limit, delta_limit=delta_limit)
    monitors.compare(32, (2560, 1440), limit=limit, delta_limit=delta_limit)
    monitors.compare(34, (3440, 1440), limit=limit, delta_limit=delta_limit)
    monitors.compare(37, (3840, 2160), limit=limit, delta_limit=delta_limit)
    monitors.compare(37.5, (3840, 1600), limit=limit, delta_limit=delta_limit)
    monitors.compare(38, (3840, 1600), limit=limit, delta_limit=delta_limit)
    monitors.compare(40, (3840, 2160), limit=limit, delta_limit=delta_limit)
    monitors.compare(40, (5120, 2160), limit=limit, delta_limit=delta_limit)
    monitors.compare(41.5, (3840, 2160), limit=limit, delta_limit=delta_limit)
    monitors.compare(42.51, (3840, 2160), limit=limit, delta_limit=delta_limit)
    monitors.compare(43, (3840, 2160), limit=limit, delta_limit=delta_limit)
    monitors.compare(49, (5120, 1440), limit=limit, delta_limit=delta_limit)
    monitors.compare(57, (7680, 2160), limit=limit, delta_limit=delta_limit)
