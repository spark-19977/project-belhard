from . import models


def categories_processor(request):
    categories = models.Category.objects.all()
    return {'categories': categories}