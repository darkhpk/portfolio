from django import template
register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    try:
        """Add a CSS class to a form field widget without losing existing ones."""
        existing = field.field.widget.attrs.get("class", "")
        return field.as_widget(attrs={"class": (existing + " " + css).strip()})
    except AttributeError:
        return field