class Languages:
    ENGLISH = "en"
    WELSH = "cy"


class Enums:
    languages = Languages()

    asset_types = [
        ('posters', 'Poster'),
        ('digital_screens', 'Digital Screen'),
        ('alternative_formats', 'Alternative Format'),
        ('digital_out_of_home', 'Digital out of home'),
        ('email_signatures', 'Email Signature'),
        ('fact_sheets', 'Fact Sheet'),
        ('leaflet', 'Leaflet(s)'),
        ('lockup', 'Lockup'),
        ('pm_letter', 'PM Letter'),
        ('press_release', 'Press Release'),
        ('radio', 'Radio'),
        ('social_media', 'Social Media'),
        ('ads', 'Ads'),
        ('web_banners', 'Web Banners'),
        ('translations', 'Translations'),
        ('pull_up_banners', 'Pull Up Banners'),
        ('artwork', 'Artwork'),
    ]


enums = Enums()
