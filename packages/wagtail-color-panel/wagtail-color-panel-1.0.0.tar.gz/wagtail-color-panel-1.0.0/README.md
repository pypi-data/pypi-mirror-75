![Wagtail-Color-Panel](https://github.com/marteinn/wagtail-color-panel/workflows/Wagtail-Color-Panel/badge.svg)

# Wagtail-Color-Panel

Introduces panels for selecting colors in Wagtail.

![Screen1](https://raw.githubusercontent.com/marteinn/wagtail-color-panel/develop/img/img-in-streamfield.png)


## Features

- NativeColorPanel that can be used in your edit handler
- NativeColorBlock for usage in a StreamField
- Based on the native HTML5 color picker
- A custom db field for improved validation


## Example

```python
from wagtail.core.models import Page

from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel


class MyPage(Page):
    color = ColorField()

    content_panels = Page.content_panels + [
        NativeColorPanel('color'),
    ]
```


## Documentation

- [Getting started](./docs/1_getting_started.md)
- [Adding panel to a Page](./docs/2_adding_to_a_page.md)
- [Adding to a StreamField](./docs/3_adding_to_a_streamfield.md)


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Wagtail-Color-Panel is released under the [MIT License](http://www.opensource.org/licenses/MIT).
