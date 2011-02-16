<!DOCTYPE HTML>
<html>
    <head>
        <title>{{ path }}</title>
        <link rel="stylesheet" href="/static/screen.css" type="text/css" media="screen" charset="utf-8">
    </head>
    <body>
        {% if folders %}
            <ol class="folders">
            {% for folder in folders %}
                <li><a href="/{{ path }}/{{ folder }}">/{{ path }}/{{ folder }}</a></li>
            {% endfor %}
            </ol>
        {% endif %}
        {% if images %}
            <ul class="images">
            {% for image in images %}
                <li class="thumb"><a href="/{{ path }}/{{ image }}"><img src="/_thumb/{{ path }}/{{ image }}" /></a></li>
            {% endfor %}
            </ul>
        {% endif %}
    </body>
</html>
