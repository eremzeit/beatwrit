from django.template import Context, Template


active_writs_template = Template("""
{% if writs %}
    <table class='mybeat_table'>
      <tr>
        <th></th>
        <th>Opener</th>
        <th>Ending</th>
        <th>Whose turn?</th>
        <th>Authors</th>
      </tr>
      {% for writ in writs %}
          <tr>
            <td class='isturncolumn'>{% if writ.settings.turntype == "rr" and  writ.get_whose_turn.pk == mbw_context.get_bwuser.pk%} (!){% endif %}</td>
            <td class='opener'><a href='{{writ.get_absolute_url}}'>{{ writ.get_first_line|truncatewords:13}}</a></td>
            <td>{{ writ.get_ending_string }}</td>
            <td>
                {% if writ.settings.turn_type == writ.settings.choices.turn_type.ROUND_ROBIN %}
                    <a href='{{writ.get_whose_turn.get_absolute_url}}'>{{ writ.get_whose_turn.get_penname}}</a>
                {% else %}
                    {% if writ.settings.turn_type == writ.settings.choices.turn_type.FREE_FOR_ALL  %}
                        (ffa)
                    {% endif %}
                {% endif %}
            </td>
            <td>{{ writ.get_participant_count }}</td>
          </tr>
      {% endfor %}
    </table>
    <div class='star'>* denotes writs that end after a period of inactivity</div>
{% else %}
    <p class='table_text'>-- no active writs --</p>
{% endif %}
""")



historic_writs_template = Template("""                     
{% if mbw_context.get_historic_writs %}
    <table class='mybeat_table'>
      <tr>
        <th></th>
        <th>Opener</th>
        <th>Words</th>
        <th>Ended</th>
      </tr>
      {% for writ in mbw_context.get_historic_writs %}
          <tr>
            <td class='isturncolumn'>{% if writ.settings.turntype == "rr" and writ.get_whose_turn.pk == mbw_context.get_bwuser.pk %} (!) {% endif %}</td>
            <td class='opener'><a href='{{writ.get_absolute_url}}'>{{ writ.get_first_line|truncatewords:13 }}</a></td>
            <td>{{ writ.get_word_count }}</td>
            <td>{{ writ.endeddate }} </td>
            <!--<td>{{ writ.endeddate|timesince }} </td>-->
          </tr>
      {% endfor %}
    </table>
    <div class='star'>* denotes writs that end after a period of inactivity</div>
{% else %}
    <p class='table_text'>-- No finished writs yet --</p>
{% endif %}
""")


circle_writs_template = Template("""
{% if mbw_context.get_friends_writs %}
    <table class='mybeat_table'>
      <tr>
        <th></th>
        <th>Opener</th>
        <th>Ending</th>
        <th>Whose turn?</th>
      </tr>

      {% for writ in mbw_context.get_friends_writs %}
          <tr>
            <td class='isturncolumn'>{% if writ.settings.turntype == "rr" and writ.get_whose_turn.pk == mbw_context.get_bwuser.pk %} (!) {% endif %}</td>
            <td class='opener'><a href='{{writ.get_absolute_url}}'>{{ writ.get_first_line|truncatewords:13}}</a></td>
            <td>{{ writ.get_ending_string }}</td>
            <td><a href='{{writ.get_whose_turn.get_absolute_url}}'>{{ writ.get_whose_turn.get_penname}}</a></td>
          </tr>
      {% endfor %}
    </table>
    <div class='star'>* denotes writs that end after a period of inactivity</div>
{% else %}
    <p class='table_text'>-- You don't have anyone in your circle who is in a writ yet  --</p>
{% endif %}
""")



community_writs_template = Template("""
{% if mbw_context.get_community_writs %}
    <table class='mybeat_table'>
      <tr>
        <th></th>
        <th>Opener</th>
        <th>Ending</th>
        <th>Whose turn?</th>
      </tr>

      {% for writ in mbw_context.get_community_writs %}
          <tr>
            <td class='isturncolumn'>{% if writ.get_user_order.0.pk == user.beatwrituser.pk and writ.settings.turntype == "rr"  %} (!) {% endif %}</td>
            <td class='opener'><a href='{{writ.get_absolute_url}}'>{{ writ.get_first_line|truncatewords:13}}</a></td>
            <td>{{ writ.get_ending_string }}</td>
            <td><a href='{{writ.get_whose_turn.get_absolute_url}}'>{{ writ.get_whose_turn.get_penname}}</a></td>
          </tr>
      {% endfor %}
    </table>
{% else %}
    <p class='table_text'>-- No community writs yet --</p>
{% endif %}
""")


class WritListWidgetHTML:
    @staticmethod
    def active_writs(writs):
        return active_writs_template.render(Context({'writs':writs}))
    @staticmethod
    def finished_writs(writs):
        return historic_writs_template.render(Context({'writs':writs}))
    @staticmethod
    def circle_writs(writs):
        return circle_writs_template.render(Context({'writs':writs}))
    @staticmethod
    def community_writs(writs):
        return community_writs_template.render(Context({'writs':writs}))


