select gr.*, g.*
from levelupapi_game g
join levelupapi_gamer gr on g.gamer_id = gr.id
join auth_user u on u.id = gr.user_id
