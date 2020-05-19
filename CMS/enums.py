class Languages:
    ENGLISH = "en"
    WELSH = "cy"


class Enums:
    languages = Languages()

    asset_types = [
        ('posters', 'Poster'),
        ('digital_screens', 'Digital Screen'),
        ('alternative_formats', 'Alternative Format'),
        ('digital_out_of_home', 'Digital out-of-home'),
        ('email_signatures', 'Email Signature'),
        ('fact_sheets', 'Fact Sheet'),
        ('leaflet', 'Leaflet'),
        ('lockup', 'Lockup'),
        ('pm_letter', 'PM Letter'),
        ('press_release', 'Press Release')
    ]


enums = Enums()
