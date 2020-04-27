class Languages:
    ENGLISH = "en"
    WELSH = "cy"


class Enums:
    languages = Languages()

    asset_types = (
        ('posters', 'Poster'),
        ('digital_screens', 'Digital Screen'),
        ('social_media', 'Social Media Resource'),
        ('web_banners', 'Web Banner'),
        ('alternative_resources', 'Alternative Resource')
    )


enums = Enums()
