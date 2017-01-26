from viewports import *


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
                    with Image.new("RGBA", outerrect.size,"#7f7f00") as n:
                        img.paste(n, outerrect.position)
                if innerrect:
                    with Image.new("RGBA", innerrect.size, "#0000ff") as n:
                        img.paste(n, innerrect.position)
                img.show(title="%s | and &" % greenrect,
                         command='/usr/bin/feh')
                with Image.new("RGBA", redrect.size, "#ff00007f") as m:
                    img.paste(m, redrect.position)
                with Image.new("RGBA", greenrect.size, "#00ff007f") as n:
                    img.paste(n, greenrect.position)
                img.show(title="%s with orig" % greenrect,
                         command='/usr/bin/feh')


sampleLayout = {
    "Left":
        Viewport(PhysicalRectangle(518, 324, 0, 86.4),
                 ScreenRectangle.from_geometry_string('1920x1200+0+320')),
    "Middle":
        Viewport(PhysicalRectangle(518, 324, 538, 0),
                 ScreenRectangle.from_geometry_string('1920x1200+1920+0')),
    "Right":
        Viewport(PhysicalRectangle(475, 267, 1096, 28.5),
                 ScreenRectangle.from_geometry_string('1920x1080+3840+60')),
    "Laptop":
        Viewport(PhysicalRectangle(346, 194, 624, 384),
                 ScreenRectangle.from_geometry_string('1920x1080+1920+1200')),
}


def show_layout(layout):
    from functools import reduce
    import operator

    scrv = reduce(operator.or_, [layout[k].screen for k in layout])
    phyv = reduce(operator.or_, [layout[k].physical for k in layout])

    with VPImage(rectangle=scrv, background=Color("gray")) as img:
        for p in [round(layout[k].screen) for k in layout]:
            with VPImage(rectangle=p, background=Color("red")) as s:
                img.rcomposite(s, p)
        img.transform(resize="500")
        display(img)

    with VPImage(rectangle=phyv, background=Color("gray")) as img:
        for p in [round(layout[k].physical) for k in layout]:
            with VPImage(rectangle=p, background=Color("red")) as s:
                img.rcomposite(s, p)
        img.transform(resize="500")
        display(img)