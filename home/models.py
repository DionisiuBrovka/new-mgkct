from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from modelcluster.fields import ParentalKey


class HomePage(Page):

    content_panels = Page.content_panels + [
        InlinePanel('gallery', label="карточка", heading="Галерея 'Главная'"),
        InlinePanel('anons_gallery', label="анонс", heading="Галерея 'Анонсы'"),
        InlinePanel('banner_gallery', label="баннер", heading="Галерея 'Баннеры'"),
    ]

    subpage_types = ['Topic']

    class Meta:
        verbose_name = 'шаблон "Главная"'


class HomePageGallery(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='gallery', verbose_name="Страница")
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name="Изображение")
    title = models.CharField(blank=True, max_length=250, verbose_name="Заголовок")
    intro = models.CharField(blank=True, max_length=250, verbose_name="Анонс")

    panels = [
        FieldPanel('image'),
        FieldPanel('title'),
        FieldPanel('intro'),
    ]

    class Meta:
        verbose_name = "Карточка"


class HomePageBannerGallery(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='banner_gallery', verbose_name="Страница")
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name="Баннер")
    title = models.CharField(blank=True, max_length=250, verbose_name="Заголовок")
    intro = models.CharField(blank=True, max_length=250, verbose_name="Анонс")

    panels = [
        FieldPanel('image'),
        FieldPanel('title'),
        FieldPanel('intro'),
    ]

    class Meta:
        verbose_name = "Банер"
        verbose_name_plural = "Банеры"


class HomePageAnonsGallery(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='anons_gallery', verbose_name="Страница")
    title = models.CharField(blank=True, max_length=250, verbose_name="Заголовок")
    link = models.URLField(blank=True, verbose_name="Ссылка")

    panels = [
        FieldPanel('title'),
        FieldPanel('link'),
    ]

    class Meta:
        verbose_name = "Анонс"
        verbose_name_plural = "Анонсы"


class Topic(Page):

    body = RichTextField(blank=True, verbose_name="Содержание страницы")

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['HomePage']
    subpage_types = ['BasicPage', 'GalleryPage', 'NewsPage', 'EventPage', 'TimeLinePage']

    class Meta:
        verbose_name = 'шаблон "Раздел"'


class BasicPage(Page):
    intro = models.CharField(blank=True, max_length=250, verbose_name="Анонс")
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], block_counts={
        'heading': {'min_num': 1},
        'image': {'max_num': 5},
    })

    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edit_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    parent_page_types = ['Topic', 'BasicPage']
    subpage_types = ['BasicPage']

    class Meta:
        verbose_name = 'шаблон "Страница"'


class GalleryPage(Page):
    intro = models.CharField(blank=True, max_length=250, verbose_name="Анонс")
    body = RichTextField(blank=True, verbose_name="Содержание страницы")

    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edit_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    parent_page_types = ['Topic', 'BasicPage']
    subpage_types = []

    class Meta:
        verbose_name = 'шаблон "Галерея"'


class NewsPage(Page):
    parent_page_types = ['Topic', 'BasicPage']
    subpage_types = ['News']

    class Meta:
        verbose_name = 'шаблон "Блок новостей"'


class News(Page):
    intro = models.CharField(blank=True, max_length=250, verbose_name="Анонс")
    body = RichTextField(blank=True, verbose_name="Содержание страницы")

    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edit_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    parent_page_types = ['NewsPage']
    subpage_types = []

    class Meta:
        verbose_name = 'Новость'


class EventPage(Page):
    parent_page_types = ['Topic', 'BasicPage']
    subpage_types = []

    class Meta:
        verbose_name = 'шаблон "Блок событий"'


class TimeLinePage(Page):
    parent_page_types = ['Topic', 'BasicPage']
    subpage_types = []

    class Meta:
        verbose_name = 'шаблон "Летопись"'