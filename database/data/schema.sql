CREATE TABLE message
(
    message_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    reaction_count INT DEFAULT 0
);

CREATE TABLE chat
(
    chat_id            BIGINT NOT NULL,
    channel_id         TEXT,
    min_reaction_count INT DEFAULT 5,
    emoji_list         TEXT[] DEFAULT array['⭐', '😁']
);