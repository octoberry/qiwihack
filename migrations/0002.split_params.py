step(
    """
    ALTER TABLE events ADD COLUMN split_event_id int4;
    ALTER TABLE events ADD COLUMN split_owner_id int4;
    ALTER TABLE events ADD COLUMN split_member_id int4;
    """
)
