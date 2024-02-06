import io

from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def create_shopping_cart(ingredients_cart):
    """Создаем список с ингредиентами."""

    response = HttpResponse(content_type='applications/pdf')
    response['Content-Disposition'] = (
        "attachment; filename='shopping_Cart.pdf'"
    )
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    page.setFont('Vera', 24)
    page.drawString(200, 800, 'Список покупок.')
    page.setFont('Vera', 14)
    from_bottom = 750
    for number, ingredient in enumerate(ingredients_cart, start=1):
        page.drawString(
            50,
            from_bottom,
            f"{number}. {ingredient['ingredient__name']}: "
            f"{ingredient['ingredient_value']} "
            f"{ingredient['ingredient__measurement_unit']}.",
        )
        from_bottom -= 20
        if from_bottom <= 50:
            from_bottom = 800
            page.showPage()
            page.setFont('Vera', 14)
    page.showPage()
    page.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
