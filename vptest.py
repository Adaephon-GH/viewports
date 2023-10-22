import subprocess
from PIL import ImageShow

from viewports import (
    Image,
    Viewport,
    ScreenRectangle,
    PhysicalRectangle,
)

class FEHViewer(ImageShow.UnixViewer):
    def get_command_ex(self, file, title=None, **options):
        command = executable = "feh"
        if title:
            command += f" --title {quote(title)}"
        return command, executable

    def show_file(self, path, **options):
        args = ["feh"]
        title = options.get("title")
        if title:
            args += ["--title", title]
        args.append(path)

        subprocess.Popen(args)
        return 1

ImageShow.register(FEHViewer(), 0)


def dummy_tester():
    with Image.open('sample.png') as orig:
        with Image.new('RGB', (640, 360), color='gray') as img:
            with orig.crop((100, 100, 150, 150)) as a:
                img.paste(a, (30, 70))
            with orig.crop((100, 100, 200, 200)) as b:
                b.resize((50, 50))
                img.paste(b, (300, 70))
            with orig.crop((10, 30, 210, 230)) as c:
                img.paste(c, (round(200 * .75), round(200 * .75)))
            img.show()


def overlap_tester():
    # Handel with care, this will open a lot of windows
    import itertools
    bigrect = ScreenRectangle.from_size(1000, 1000)
    redrect = ScreenRectangle(300, 300, 700, 700)
    for l, t in itertools.combinations_with_replacement(
            [100, 400, 800], 2):
        for r, b in itertools.combinations_with_replacement(
                [200, 600, 900], 2):
            greenrect = ScreenRectangle(l, t, r, b)
            outerrect = redrect | greenrect
            innerrect = redrect & greenrect
            with Image.new("RGBA", bigrect.size, "gray") as img:
                if outerrect:
                    with Image.new("RGBA", outerrect.size, "#7f7f00") as n:
                        img.paste(n, outerrect.position)
                if innerrect:
                    with Image.new("RGBA", innerrect.size, "#0000ff") as n:
                        img.paste(n, innerrect.position)
                img.show(title="%s | and &" % greenrect)
                with Image.new("RGBA", redrect.size, "#ff00007f") as m:
                    img.paste(m, redrect.position)
                with Image.new("RGBA", greenrect.size, "#00ff007f") as n:
                    img.paste(n, greenrect.position)
                img.show(title="%s with orig" % greenrect)


sampleLayout1s = {
    "Left":
        Viewport(PhysicalRectangle(0, 40,
                                   518.4, 364),
                 ScreenRectangle.from_geometry_string('1920x1200+0+0')),
    "Middle":
        Viewport(PhysicalRectangle(518.4+16, 40,
                                   518.4+16+518.4, 364),
                 ScreenRectangle.from_geometry_string('1920x1200+1920+0')),
    "Right":
        Viewport(PhysicalRectangle(2*518.4+16+24, 58.5,
                                   2*518.4+16+24+475, 58.5+267),
                 ScreenRectangle.from_geometry_string('1920x1080+3840+60')),
    "Laptop":
        Viewport(PhysicalRectangle(518.4+7.7+89, 417,
                                   518.4+7.7+89+346, 417+194),
                 ScreenRectangle.from_geometry_string('1920x1080+1920+1200')),
}


sampleLayout1 = {
    "Left":
        Viewport(PhysicalRectangle(0, 0,
                                   518.4, 324),
                 ScreenRectangle.from_geometry_string('1920x1200+0+0')),
    "Middle":
        Viewport(PhysicalRectangle(518.4+16, 0,
                                   518.4+16+518.4, 324),
                 ScreenRectangle.from_geometry_string('1920x1200+1920+0')),
    "Right":
        Viewport(PhysicalRectangle(2*518.4+16+24, 18.5,
                                   2*518.4+16+24+475, 18.5+267),
                 ScreenRectangle.from_geometry_string('1920x1080+3840+60')),
    "Laptop":
        Viewport(PhysicalRectangle(518.4+7.7+89, 377,
                                   518.4+7.7+89+346, 377+194),
                 ScreenRectangle.from_geometry_string('1920x1080+1920+1200')),
}


sampleLayout2 = {
    "Left":
        Viewport(PhysicalRectangle(0, 0, 301, 376),
                 ScreenRectangle.from_geometry_string('1024x1280+0+0')),
    "Main":
        Viewport(PhysicalRectangle(387, 0, 597 + 387, 336),
                 ScreenRectangle.from_geometry_string('2560x1440+1024+0'))
}

layoutOffice = {
    "Left": Viewport(PhysicalRectangle(0,0,5184,3240),ScreenRectangle.from_geometry_string('1920x1200+0+0')),
    "Main": Viewport(PhysicalRectangle(5184+124,0,5184*2+124,3240),ScreenRectangle.from_geometry_string('1920x1200+1920+0')),
    "Right": Viewport(PhysicalRectangle(5184*2+124*2,0,5184*3+124*2,3240),ScreenRectangle.from_geometry_string('1920x1200+3840+0')),
    "Laptop": Viewport(PhysicalRectangle(5184//2*3-3446//2+124,3240+100,5184//2*3+3446//2+124,3240+100+2154),ScreenRectangle.from_geometry_string('1920x1200+1920+1200')),
}

layoutOffice1 = {
    "Left": Viewport(PhysicalRectangle(0,0,5184,3240),ScreenRectangle.from_geometry_string('1920x1200+0+0')),
    "Main": Viewport(PhysicalRectangle.from_size_and_position((5184,3240), (5184+124,0)),ScreenRectangle.from_geometry_string('1920x1200+1920+0')),
    "Right": Viewport(PhysicalRectangle.from_size_and_position((5184,3240), ((5184+124)*2,0)),ScreenRectangle.from_geometry_string('1920x1200+3840+0')),
    "Laptop": Viewport(PhysicalRectangle.from_size_and_position((3446, 2154), (5184+124+(5184-3446)//2,3240+100)),ScreenRectangle.from_geometry_string('1920x1200+1920+1200')),
}

# Use real size for Laptop display but appearant distance between Laptop and Main
layoutHomeActualSize = {
    "Laptop": Viewport(PhysicalRectangle.from_size_and_position((3446,2154), (0, 450)),ScreenRectangle.from_geometry_string('1920x1200+0+0')),
    "Main": Viewport(PhysicalRectangle.from_size_and_position((5968, 3357), (3446+600, 0)), ScreenRectangle.from_geometry_string('2560x1440+1920+0')),
    "Right": Viewport(PhysicalRectangle.from_size_and_position((4768, 2682), (3446+600+5968+430, 0)), ScreenRectangle.from_geometry_string('1920x1080+4480+0')),
}

# Use appearant size (using Main as reference) for Laptop display and appearant distance between Laptop and Main
layoutHomeAppearantSize = {
    "Laptop": Viewport(PhysicalRectangle.from_size_and_position((3000, 1875), (0,450)),ScreenRectangle.from_geometry_string('1920x1200+0+0')),
    "Main": Viewport(PhysicalRectangle.from_size_and_position((5968, 3357), (3000+600, 0)), ScreenRectangle.from_geometry_string('2560x1440+1920+0')),
    "Right": Viewport(PhysicalRectangle.from_size_and_position((4768, 2682), (3000+600+5968+430, 0)), ScreenRectangle.from_geometry_string('1920x1080+4480+0')),
}

layoutLaptopOnly = {
    "Laptop": Viewport(PhysicalRectangle.from_size_and_position((3446, 2154), (0, 0)),ScreenRectangle.from_geometry_string('1920x1200+0+0')),
}


def colorGen():
    colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'white']
    for c in colors:
        yield c

def show_layout(layout):
    from functools import reduce
    import operator

    scrv = reduce(operator.or_, [layout[k].screen for k in layout])
    phyv = reduce(operator.or_, [layout[k].physical for k in layout])

    with Image.new("RGBA", scrv.size, "gray") as img:
        color = colorGen()
        for p in [round(layout[k].screen) for k in layout]:
            with Image.new("RGBA", p.size, next(color)) as s:
                img.paste(s, p.position)
         ## img = img.resize((768, round(img.height*768/img.width)))
        img.show(title="screen")

    with Image.new("RGBA", phyv.intsize, "gray") as img:
        color = colorGen()
        for p in [round(layout[k].physical) for k in layout]:
            with Image.new("RGBA", p.intsize, next(color)) as s:
                img.paste(s, p.position)
        img = img.resize((1920, round(img.height*1920/img.width)))
        img.show(title="phys")
