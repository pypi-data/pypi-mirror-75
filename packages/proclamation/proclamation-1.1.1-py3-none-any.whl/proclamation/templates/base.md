{#-
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Proclamation contributors
-#}
{% macro format_ref(ref) -%}
    {%- if ref.item_type == "issue" -%}
        {%- set subdir = "issues" %}
        {%- set link_text %}#{{ ref.number }}{% endset %}
    {%- elif ref.item_type == "pr" -%}
        {%- set subdir = "pull" %}
        {%- set link_text %}#{{ ref.number }}{% endset %}
    {%- elif ref.item_type == "mr" -%}
        {%- set subdir = "merge_requests" %}
        {%- set link_text %}!{{ ref.number }}{% endset %}
    {%- endif -%}
[{{ link_text }}]({{base_url}}/{{subdir}}/{{ ref.number }})
{%- endmacro -%}
{% macro format_refs(refs) -%}
    {% if (refs | length) > 0 %}
        {%- set comma = joiner(",\n") -%}
        {% for ref in refs -%}
            {{comma()}}{{format_ref(ref)}}
        {%- endfor %}
    {%- endif %}
{%- endmacro -%}
{% block title %}## {{ project_name }} {{project_version}} ({{date}}){% endblock %}
{% block sections_and_fragments -%}
{%- for section in sections %}
- {{ section.name }}
{%- for fragment in section.fragments %}
  - {{ fragment.text | wordwrap | indent }}
    ({{ format_refs(fragment.refs) | indent }})
{%- else %}
  - No significant changes
{%- endfor -%}
{%- endfor %}{% endblock %}
