from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Genre, Movie, MovieShort, Actor, Rating, RatingStar, Reviews
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Description', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url',)
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    model = Reviews
    readonly_fields = ('name', 'email')
    extra = 1


class MovieShortInline(admin.TabularInline):
    model = MovieShort
    extra = 1
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='100' height='110'>")

    get_image.short_description = 'Image'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShortInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    readonly_fields = ('get_image', )
    # fields = (('actors', 'directors', 'genres'),)
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'),)
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ("Actors", {
            'classes': ('collapse', ),
            'fields': (('directors', 'actors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ("Option", {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.poster.url} width='100' height='110'>")

    def unpublish(self, request, queryset):
        """Unpublish"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запесь была обнавлена'
        else:
            message_bit = f'{row_update} запесей были обнавлены'
        self.message_user(request, f'{row_update}')

    def publish(self, request, queryset):
        """Publish"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запесь была обнавлена'
        else:
            message_bit = f'{row_update} запесей были обнавлены'
        self.message_user(request, f'{row_update}')

    publish.short_description = 'Опубликовать'
    publish.allow_permissions = ('change',)

    unpublish.short_description = 'Сняты с публикаций'
    unpublish.allow_permissions = ('change',)

    get_image.short_description = 'Image'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', )


@admin.register(MovieShort)
class MovieShortAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'get_image', 'movie')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='50' height='60'>")

    get_image.short_description = 'Image'


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='50' height='60'>")

    get_image.short_description = 'Image'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'ip')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value', )


admin.site.site_title = "Django Movie"
admin.site.site_header = "Django Movie"
