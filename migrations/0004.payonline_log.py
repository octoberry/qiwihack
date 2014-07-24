step(
    """
    CREATE SEQUENCE payonline_log_id_seq;
    CREATE TABLE payonline_log (
        "id" int4 NOT NULL DEFAULT nextval('payonline_log_id_seq'),
        "event_id" int4 NOT NULL,
        "operation" varchar(255) NOT NULL,
        "request" text NOT NULL,
        "response" text NOT NULL,
        "created_at" timestamp(6) NOT NULL default CURRENT_TIMESTAMP,
        CONSTRAINT "payonline_log_pkey" PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE
    )
    WITH (OIDS=FALSE);
    ALTER SEQUENCE payonline_log_id_seq OWNED BY payonline_log.id;
    ALTER TABLE payonline_log ADD CONSTRAINT payonline_log_event_id_fkey FOREIGN KEY(event_id) REFERENCES events(id) on delete cascade;
    """
)
