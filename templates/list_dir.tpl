<!DOCTYPE HTML>
<html>
    <head>
        <title>{{ path }}</title>
        <link rel="stylesheet" href="/static/css/screen.css" type="text/css" media="screen" charset="utf-8">
    </head>
    <body>
        {% if folders or path %}
            <ol class="folders">
            {% if path %}
            <li><a href="/{{ path }}/../">./</a></li>
            {% endif %}
            {% for folder in folders %}
                <li><a href="{% if path %}/{% endif %}{{ path }}/{{ folder }}">{{ path|escape }}/{{ folder|escape }}</a></li>
            {% endfor %}
            </ol>
        {% endif %}
        {% if images %}
            <ul class="images">
            {% for image in images %}
                <li class="thumb"><a href="{% if path %}/{% endif %}{{ path }}/{{ image }}"><img src="/_thumb/{{ path }}/{{ image }}" /></a></li>
            {% endfor %}
            </ul>
        {% endif %}
    </body>
</html>
